import React, { useState } from 'react';
import { 
  Container, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  Box,
  Grid,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  CircularProgress,
  Tooltip
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import DownloadIcon from '@mui/icons-material/Download';
import CancelIcon from '@mui/icons-material/Cancel';

function App() {
  const [invoices, setInvoices] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [processing, setProcessing] = useState(false);
  const [editingIndex, setEditingIndex] = useState(null);
  const [downloading, setDownloading] = useState(false);

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    setError('');
    setSuccess('');
    setProcessing(true);

    const formData = new FormData();
    acceptedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await axios.post('http://localhost:8000/upload/bulk/', formData);
      setInvoices(response.data.map((result, index) => ({
        ...result,
        status: result.error ? 'failed' : 'complete',
        originalFile: acceptedFiles[index]
      })));
      setSuccess(`Successfully processed ${response.data.length} files`);
    } catch (err) {
      setError('Error processing invoices: ' + err.message);
    } finally {
      setProcessing(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    multiple: true
  });

  const handleInputChange = (index, field, value) => {
    setInvoices(prev => prev.map((invoice, i) => 
      i === index ? { ...invoice, [field]: value } : invoice
    ));
  };

  const handleEdit = (index) => {
    setEditingIndex(index);
  };

  const handleSave = async () => {
    try {
      const validInvoices = invoices
        .filter(inv => !inv.error)
        .map(({ originalFile, status, ...rest }) => rest);
      
      await axios.post('http://localhost:8000/save/bulk/', {
        invoices: validInvoices
      });
      
      setSuccess('All invoices saved successfully!');
      setInvoices([]);
      setEditingIndex(null);
    } catch (err) {
      setError('Error saving invoices: ' + err.message);
    }
  };

  const handleDownload = async () => {
    try {
      setDownloading(true);
      setError('');
      
      // Make the request to get the CSV file
      const response = await axios.get('http://localhost:8000/download/latest/', {
        responseType: 'blob'
      });
      
      // Create a blob from the response data
      const blob = new Blob([response.data], { type: 'text/csv' });
      
      // Create a download link and trigger the download
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'processed_invoices.csv');
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      setSuccess('CSV file downloaded successfully!');
    } catch (err) {
      setError('Error downloading CSV: ' + err.message);
    } finally {
      setDownloading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'waiting': return '⏳';
      case 'processing': return '🔄';
      case 'complete': return '✅';
      case 'failed': return '❌';
      default: return '⏳';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Invoice Processing Tool
      </Typography>

      <Paper 
        {...getRootProps()} 
        sx={{ 
          p: 3, 
          mb: 3, 
          textAlign: 'center',
          backgroundColor: isDragActive ? '#f0f8ff' : '#fafafa',
          border: '2px dashed #ccc',
          cursor: 'pointer'
        }}
      >
        <input {...getInputProps()} />
        <Typography>
          {isDragActive
            ? "Drop the invoice files here"
            : "Drag and drop invoice files here, or click to select multiple files"}
        </Typography>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      {processing && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
          <CircularProgress />
        </Box>
      )}

      {invoices.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">
              Processed Invoices ({invoices.length})
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Tooltip title="Download CSV">
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={handleDownload}
                  disabled={downloading}
                >
                  {downloading ? 'Downloading...' : 'Download CSV'}
                </Button>
              </Tooltip>
              <Button
                variant="contained"
                startIcon={<SaveIcon />}
                onClick={handleSave}
                disabled={invoices.some(inv => inv.error)}
              >
                Save All
              </Button>
            </Box>
          </Box>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Status</TableCell>
                  <TableCell>File Name</TableCell>
                  <TableCell>Invoice Number</TableCell>
                  <TableCell>Date</TableCell>
                  <TableCell>Vendor</TableCell>
                  <TableCell>Amount</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {invoices.map((invoice, index) => (
                  <TableRow key={index}>
                    <TableCell>{getStatusIcon(invoice.status)}</TableCell>
                    <TableCell>{invoice.filename}</TableCell>
                    <TableCell>
                      {editingIndex === index ? (
                        <TextField
                          value={invoice.invoice_number}
                          onChange={(e) => handleInputChange(index, 'invoice_number', e.target.value)}
                          size="small"
                        />
                      ) : invoice.invoice_number}
                    </TableCell>
                    <TableCell>
                      {editingIndex === index ? (
                        <TextField
                          value={invoice.invoice_date}
                          onChange={(e) => handleInputChange(index, 'invoice_date', e.target.value)}
                          size="small"
                        />
                      ) : invoice.invoice_date}
                    </TableCell>
                    <TableCell>
                      {editingIndex === index ? (
                        <TextField
                          value={invoice.vendor_name}
                          onChange={(e) => handleInputChange(index, 'vendor_name', e.target.value)}
                          size="small"
                        />
                      ) : invoice.vendor_name}
                    </TableCell>
                    <TableCell>
                      {editingIndex === index ? (
                        <TextField
                          value={invoice.total_amount}
                          onChange={(e) => handleInputChange(index, 'total_amount', e.target.value)}
                          size="small"
                        />
                      ) : invoice.total_amount}
                    </TableCell>
                    <TableCell>
                      {!invoice.error && (
                        <IconButton
                          onClick={() => handleEdit(index)}
                          disabled={processing}
                        >
                          <EditIcon />
                        </IconButton>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}
    </Container>
  );
}

export default App; 