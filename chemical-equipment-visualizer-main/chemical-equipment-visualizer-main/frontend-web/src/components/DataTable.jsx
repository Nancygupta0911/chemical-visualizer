import React, { useState } from 'react';
import './DataTable.css';

function DataTable({ data }) {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;

  const sortedData = React.useMemo(() => {
    let sortableData = [...data];
    if (sortConfig.key) {
      sortableData.sort((a, b) => {
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];
        
        if (typeof aValue === 'number' && typeof bValue === 'number') {
          return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
        }
        
        const aStr = String(aValue).toLowerCase();
        const bStr = String(bValue).toLowerCase();
        
        if (aStr < bStr) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aStr > bStr) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }
    return sortableData;
  }, [data, sortConfig]);

  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const indexOfLastRow = currentPage * rowsPerPage;
  const indexOfFirstRow = indexOfLastRow - rowsPerPage;
  const currentRows = sortedData.slice(indexOfFirstRow, indexOfLastRow);
  const totalPages = Math.ceil(sortedData.length / rowsPerPage);

  const getSortIcon = (columnKey) => {
    if (sortConfig.key !== columnKey) return '⇅';
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  return (
    <div className="data-table-container">
      <h2>Equipment Data</h2>
      <div className="table-info">
        Showing {indexOfFirstRow + 1}-{Math.min(indexOfLastRow, data.length)} of {data.length} entries
      </div>
      
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th onClick={() => requestSort('Equipment Name')}>
                Equipment Name {getSortIcon('Equipment Name')}
              </th>
              <th onClick={() => requestSort('Type')}>
                Type {getSortIcon('Type')}
              </th>
              <th onClick={() => requestSort('Flowrate')}>
                Flowrate {getSortIcon('Flowrate')}
              </th>
              <th onClick={() => requestSort('Pressure')}>
                Pressure {getSortIcon('Pressure')}
              </th>
              <th onClick={() => requestSort('Temperature')}>
                Temperature {getSortIcon('Temperature')}
              </th>
            </tr>
          </thead>
          <tbody>
            {currentRows.map((row, index) => (
              <tr key={index}>
                <td>{row['Equipment Name']}</td>
                <td>{row['Type']}</td>
                <td>{typeof row['Flowrate'] === 'number' ? row['Flowrate'].toFixed(2) : row['Flowrate']}</td>
                <td>{typeof row['Pressure'] === 'number' ? row['Pressure'].toFixed(2) : row['Pressure']}</td>
                <td>{typeof row['Temperature'] === 'number' ? row['Temperature'].toFixed(2) : row['Temperature']}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span className="page-info">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default DataTable;