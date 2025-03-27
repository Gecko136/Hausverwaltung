# Hausverwaltung - Property Management System

## Description
Hausverwaltung is a comprehensive property management system built to handle tenant agreements, manage apartment and house data, and generate utility cost statements (Nebenkostenabrechnungen) for residential properties. The system also supports various reports and integrates with a database backend to manage the data efficiently.

## Features
- **Tenant Management**: Handle Mietverträge (lease agreements) with detailed information about tenants.
- **Property Management**: Manage apartments (Wohnungen) and houses (Häuser), including their details and associated rooms.
- **Nebenkostenabrechnung**: Calculate utility costs and generate cost reports for tenants.
- **Database Integration**: Interacts with a backend database to store and retrieve tenant, property, and utility data.
- **Command-line Interface**: Interact with the system through a CLI, making it easy to generate reports and perform system operations.

## Installation

### Requirements
- Python 3.x
- pip (Python package manager)

### Install Dependencies
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hausverwaltung.git
   cd hausverwaltung
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On MacOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
Make sure to configure your database and application settings in the `config.ini` file. This file contains important configurations for your system to work properly.

## Usage

### Running the CLI
The system is primarily accessed through the command line interface (CLI). To use the application, use the following structure:

```bash
immo <command> <subcommand> [options]
```

### Available Commands

- **Report Generation**
    - To generate a Nebenkosten (utility cost) report for a tenant in PDF format:
      ```bash
      immo report nebenkosten mieter --id {id} --pdf
      ```
      Where `{id}` is the ID of the tenant whose Nebenkosten report you want to generate.

### Example Commands

1. **Generate Nebenkosten report for a specific tenant**:
   ```bash
   immo report nebenkosten mieter --id 123 --pdf
   ```
   This will calculate the Nebenkosten for the tenant with ID `123` and generate a PDF report.

## Contributing
We welcome contributions to this project. Please follow the steps below to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Python
- ReportLab for PDF generation
- Jinja2 for templating (if applicable)

