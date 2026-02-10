from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponse
from .models import Dataset
from .serializers import DatasetSerializer, DatasetListSerializer
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [AllowAny]  # ✅ Changed from IsAuthenticated
    
    def list(self, request):
        """List last 5 datasets"""
        datasets = Dataset.objects.all()[:5]
        serializer = DatasetListSerializer(datasets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload and process CSV file"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Validate file extension
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV using pandas
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing columns: {", ".join(missing_columns)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convert dataframe to JSON
            data = df.to_dict('records')
            
            # Calculate summary statistics
            summary = {
                'total_count': len(df),
                'avg_flowrate': float(df['Flowrate'].mean()),
                'avg_pressure': float(df['Pressure'].mean()),
                'avg_temperature': float(df['Temperature'].mean()),
                'type_distribution': df['Type'].value_counts().to_dict(),
                'max_flowrate': float(df['Flowrate'].max()),
                'min_flowrate': float(df['Flowrate'].min()),
                'max_pressure': float(df['Pressure'].max()),
                'min_pressure': float(df['Pressure'].min()),
                'max_temperature': float(df['Temperature'].max()),
                'min_temperature': float(df['Temperature'].min()),
            }
            
            # Create dataset
            dataset = Dataset.objects.create(
                filename=csv_file.name,
                data=data,
                summary=summary
            )
            
            # Cleanup old datasets (keep only last 5)
            Dataset.cleanup_old_datasets()
            
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get summary for a specific dataset"""
        dataset = self.get_object()
        return Response(dataset.summary)
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Generate PDF report for a dataset"""
        dataset = self.get_object()
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"<b>Chemical Equipment Report</b><br/>{dataset.filename}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Summary statistics
        summary_text = f"""
        <b>Summary Statistics</b><br/>
        Total Equipment: {dataset.summary['total_count']}<br/>
        Average Flowrate: {dataset.summary['avg_flowrate']:.2f}<br/>
        Average Pressure: {dataset.summary['avg_pressure']:.2f}<br/>
        Average Temperature: {dataset.summary['avg_temperature']:.2f}<br/>
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Equipment type distribution
        elements.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
        type_data = [['Type', 'Count']]
        for eq_type, count in dataset.summary['type_distribution'].items():
            type_data.append([eq_type, str(count)])
        
        type_table = Table(type_data)
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 12))
        
        # Equipment data table (first 10 rows)
        elements.append(Paragraph("<b>Equipment Data (First 10 Rows)</b>", styles['Heading2']))
        data_table = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        for i, row in enumerate(dataset.data[:10]):
            data_table.append([
                row['Equipment Name'],
                row['Type'],
                f"{row['Flowrate']:.2f}",
                f"{row['Pressure']:.2f}",
                f"{row['Temperature']:.2f}"
            ])
        
        equipment_table = Table(data_table)
        equipment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        elements.append(equipment_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
        return response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'ok', 'message': 'Backend is running'})