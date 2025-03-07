  # Bookstore Management System

## Overview
The Bookstore Management System is a comprehensive web application for managing bookstore operations, including inventory management, online book ordering, in-store sales, and statistical reporting. The system is built with pure JavaScript, HTML, and CSS, using Bootstrap for responsive design.

## Features

### 1. Book Inventory Management
- **Import Books**: Add new books to inventory with minimum quantity rules
- **Book Management**: Add, edit, and delete books in the system
- **System Settings**: Configure rules for minimum import quantities and order cancellation times

### 2. Online Book Ordering
- **Book Catalog**: Browse and search books by title, author, or category
- **Shopping Cart**: Add books to cart, adjust quantities, and checkout
- **Order Tracking**: View order history and status
- **Payment Options**: Choose between online payment or cash on delivery

### 3. In-store Book Sales
- **Barcode Scanning**: Quickly add books to cart using barcode scanner
- **Customer Information**: Optionally record customer details for receipts
- **Receipt Printing**: Generate and print receipts for completed sales
- **Inventory Tracking**: Automatically update inventory after sales

### 4. Statistics and Reporting
- **Revenue Reports**: View revenue by book category with charts and tables
- **Book Frequency Reports**: Track most popular books by sales frequency
- **Period Selection**: Filter reports by month and year

## System Architecture

### File Structure



### Technologies Used
- **HTML5**: Structure and content
- **CSS3**: Styling and responsive design
- **JavaScript**: Client-side functionality and data management
- **Bootstrap 5**: UI components and responsive grid
- **Chart.js**: Data visualization for reports

## User Interfaces

### Manager Interface
- Book import with quantity rules
- Book catalog management
- System settings configuration
- Revenue and sales frequency reports

### Customer Interface
- Book browsing and searching
- Shopping cart management
- Order placement and tracking
- Payment method selection

### Staff Interface
- Barcode scanning for quick sales
- Cart management
- Receipt generation
- Customer information recording

## Implementation Details

### Data Management
- Mock data stored in `data.js`
- Local state management for cart and orders
- JavaScript functions for data manipulation and display

### User Experience
- Responsive design for all device sizes
- Intuitive navigation between sections
- Real-time feedback for user actions
- Form validation for data entry

### Reporting
- Interactive charts for data visualization
- Tabular data presentation
- Filtering by time period
- Export functionality for reports

## Setup and Installation

1. Clone the repository
2. No build process required - open `index.html` in a web browser
3. For production use, deploy the files to a web server

## Browser Compatibility
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Future Enhancements
- Backend integration with database
- User authentication and role-based access
- Inventory alerts and notifications
- Advanced reporting and analytics
- Integration with payment gateways

## License
This project is licensed under the MIT License - see the LICENSE file for details.