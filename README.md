# dbc2xls

Command-line tool to convert a CAN DBC file into an Excel workbook (.xlsx) with:
- Messages (IDs, DLC, cycle times, senders, comments, etc.)
- Signals (start bit, length, scaling, units, receivers, multiplexing, choices/value tables, comments, etc.)
- Nodes
- Attributes (message/signal/node attribute key-values)
- Value tables (flattened choices)

- CLI: dbc2xlsx -i input.dbc -o output.xlsx
-      dbc2xlsx -i input.dbc -o output.xlsx --log-level DEBUG


## Install (editable)
```bash
pip install -e .
