import struct
import datetime

def extract_timestamp(hex_dump, offset):
    # Extract the timestamp bytes
    timestamp_bytes = bytes.fromhex(hex_dump[offset * 3 : (offset + 8) * 3].strip())

    # Ensure the length is correct
    if len(timestamp_bytes) != 8:
        raise ValueError("Invalid timestamp length")

    # Unpack the timestamp as a little-endian unsigned long long (Q)
    timestamp_value = struct.unpack("<Q", timestamp_bytes)[0]

    # Convert the timestamp to a human-readable format
    timestamp_readable = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp_value / 10)

    # Return the results
    return timestamp_bytes, timestamp_readable

# Define the offset for the timestamp in the hex dump
timestamp_offset = 0x140  # Assuming the timestamp starts at offset 0x140

# Replace this with your actual hex dump
your_hex_dump = """
FFD8FFE000104A464946000101006000600000FFE1107C4578696600004D4D002A00000008000301120003000000010001000001310002000000070000003287690004000000010000003A000000CA5069636173610000069000000700000430323230A0010003000001000100010000A0020004000001000000078DA003000400000100000500A005000400000100000088A420000200000021000000A8000000000200010002000000045239380000020007000000043031303000000000006132663862346366346533653531653330303030303030303030303030303030303000000000000010300003003000000010018000001200100280003000000010000002802020004000000010000000100020F4C0000000000000048000000010000004800000001FFD8FFDB00430008060607060707090809080A0C140D0C0B0B0C1912130F141D1A1F1E1D1A1C1C20
"""

# Extract and print the timestamp
timestamp_bytes, timestamp_readable = extract_timestamp(your_hex_dump, timestamp_offset)
print("Timestamp (HEX):", timestamp_bytes.hex())
print("Timestamp (Readable):", timestamp_readable)
