# Plot_CAN_Trace_from_PCAN
## Introduction
- Read logged data from CAN bus, called CAN trace, with using a PCAN adapter. 
(There are many kinds of CAN adatpers like CANNOE, CANalzyer, IXXAT, etc,. but this is only for the data collected thorugh PCAN USB adapter from Peak Systems)
- The extension of the CAN trace is *.trc
- Plot a SPN (suspect parameter number) with inputs of PGN (Parameter Group Number) and start byte/start bit/length of the SPN.
(I could have devloped a function to search corresponding PGN and start byte/start bit/length of the SPN based on J1939DA, but I am not sure it would be okay to do so because J1939DA is something our company bought a license for. This also would allow users to plot any SPNs even not defined in the industrial standard) 

## Author
- Name : Sanghyeok Lee
- Company : Cummins Korea
