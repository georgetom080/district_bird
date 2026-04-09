#!/usr/bin/env python3
"""
Script to find species with highest percentage occurrence in checklists
from a specific county (or all counties except one) in the eBird TSV format data file.
"""

import sys
import argparse
from collections import Counter, defaultdict

def main(county_name, num_species, invert_county=False):
    # File path
    data_file = 'ebd_IN-TN_relFeb-2026.txt'

    try:
        # Track species per checklist
        checklist_species = defaultdict(set)  # checklist_id -> set of species
        total_records = 0
        county_records = 0

        with open(data_file, 'r', encoding='utf-8') as f:
            # Read header to identify column indices
            header = f.readline().strip().split('\t')

            # Find column indices
            try:
                common_name_idx = header.index('COMMON NAME')
                county_idx = header.index('COUNTY')
                checklist_id_idx = header.index('SAMPLING EVENT IDENTIFIER')
            except ValueError as e:
                print(f"Error: Column not found in header - {e}")
                sys.exit(1)

            # Process each record
            for line in f:
                total_records += 1
                fields = line.strip().split('\t')

                # Skip if not enough fields
                if len(fields) <= max(common_name_idx, county_idx, checklist_id_idx):
                    continue

                county = fields[county_idx].strip()

                # Filter for specified county (or exclude it if inverted)
                county_matches = county.lower() == county_name.lower()
                should_process = county_matches if not invert_county else not county_matches

                if should_process:
                    county_records += 1
                    species_name = fields[common_name_idx].strip()
                    checklist_id = fields[checklist_id_idx].strip()

                    # Only process if species name and checklist ID are not empty
                    if species_name and checklist_id:
                        checklist_species[checklist_id].add(species_name)

        # Calculate species occurrence percentages
        total_checklists = len(checklist_species)
        species_percentage = {}

        for checklist_id, species_set in checklist_species.items():
            for species in species_set:
                if species not in species_percentage:
                    species_percentage[species] = 0
                species_percentage[species] += 1

        # Convert counts to percentages
        for species in species_percentage:
            species_percentage[species] = (species_percentage[species] / total_checklists) * 100

        # Display results
        location_desc = f"excluding {county_name}" if invert_county else f"{county_name}"
        print(f"\n{'='*80}")
        print(f"eBird Data Analysis - {location_desc} County, Tamil Nadu")
        print(f"Species Occurrence by Checklist Percentage")
        print(f"{'='*80}")
        print(f"Total records processed: {total_records:,}")
        print(f"Records from {location_desc}: {county_records:,}")
        print(f"Unique checklists: {total_checklists:,}")
        print(f"Unique species found: {len(species_percentage)}")
        print(f"\n{'='*80}")
        print(f"{'RANK':<6}{'SPECIES':<50}{'PERCENTAGE':>15}")
        print(f"{'='*80}")

        # Get top N species by percentage
        top_species = sorted(species_percentage.items(),
                           key=lambda x: x[1], reverse=True)[:num_species]

        if not top_species:
            print(f"No species found for {location_desc} county.")
            return

        for rank, (species, percentage) in enumerate(top_species, 1):
            print(f"{rank:<6}{species:<50}{percentage:>14.2f}%")

        print(f"{'='*80}\n")

        # Summary statistics
        if top_species:
            avg_percentage = sum(percentage for _, percentage in top_species) / len(top_species)
            print(f"Average percentage (top {num_species}): {avg_percentage:.2f}%")
            print(f"Highest occurrence: {top_species[0][0]} ({top_species[0][1]:.2f}%)")
            print(f"Lowest in top {num_species}: {top_species[-1][0]} ({top_species[-1][1]:.2f}%)")
            print(f"Species in 100% of checklists: {sum(1 for _, pct in top_species if pct >= 100.0)}")

    except FileNotFoundError:
        print(f"Error: Data file '{data_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find species with highest percentage occurrence in checklists from eBird TSV data. Use --invert to exclude the specified county.'
    )
    parser.add_argument(
        '-c', '--county',
        type=str,
        default='Krishnagiri',
        help='County name (default: Krishnagiri)'
    )
    parser.add_argument(
        '-n', '--number',
        type=int,
        default=50,
        help='Number of top species to display (default: 50)'
    )
    parser.add_argument(
        '-i', '--invert',
        action='store_true',
        help='Invert county selection (show species from all counties EXCEPT the specified one)'
    )

    args = parser.parse_args()
    main(args.county, args.number, args.invert)
