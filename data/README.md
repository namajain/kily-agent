# Data Directory

This directory contains all data files used by the system, organized by profile and type.

## Structure

```
data/
├── profiles/                    # Profile-specific data
│   ├── profile1/               # Sales Data Analysis profile
│   │   ├── sales.csv
│   │   ├── regions.csv
│   │   └── products.csv
│   ├── profile2/               # Customer Analytics profile
│   │   ├── this_month_keyword_summary.csv
│   │   └── this_week_keyword_summary.csv
│   └── profile3/               # Financial Reports profile
│       └── financial.csv
├── samples/                    # Generic sample data
│   ├── customers.csv
│   ├── purchases.csv
│   ├── feedback.csv
│   └── support.csv
└── README.md                   # This file
```

## Usage

- **Profile data**: Used by specific profiles, referenced in database
- **Sample data**: Generic data for testing and development
- **Downloads**: Temporary storage for dynamic file downloads (not in this directory)

## Data Sources

Each profile's data sources are defined in the database and point to files in this directory using `file://` URLs.

Example:
```json
{
  "url": "file://data/profiles/profile1/sales.csv",
  "filename": "sales.csv",
  "description": "Sales data for analysis"
}
```
