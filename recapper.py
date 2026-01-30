from scapy.all import TCP, rdpcap                                                   # rdpcap is the func that reads a PCAP file into memory.
import collections                                                                  # To create a namedtuple, which make the data more readable than a list or dict.
import os
import re                                                                           # For regular expressions: a tool for manipulating text patterns within strings. 
import sys  
import zlib                                                                         # Handles the decompression of HTTP traffic  that has been zipped to save bandwidth.

OUTDIR = '/home/kali/Desktop/pictures'                                              # Where the extracted images will go.
PCAPS = '/home/kali/Downloads'                                                      # Where the source PCAP files are have to be located.

Response = collections.namedtuple('Response', ['header', 'payload'])                # This object represents a single HTTP response. 

# HTTP Header extraction
def get_header(payload):                                                            # Raw bytes to process.
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]                         # Searches for the double carriage-return line-feed, which marks the end of an HTTP header and the start of the body, isolating the HTTP header from the body. 
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()                                                          # To ensure that we get real-time feedback on the screen, giving us instant visual updates.
        return None 
    # This Regular Expression transforms a block of text into a Python dictionary:
    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', 
                             header_raw.decode()))
    if 'Content-Type' not in header:
        return None
    return header


def extract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']:
        content_type = Response.header['Content-Type'].split('/')[1]
        content = Response.payload[Response.payload.index(b'\r\n\r\n')+4:]
    
        if 'Content-Encoding' in Response.header:
            if Response.header['Content-Encoding'] == "gzip":
                content = zlib.decompress(content, zlib.MAX_WBITS | 32) 
            elif Response.header['Content-Encoding'] == "deflate":
                content = zlib.decompress(content)
        
    return content, content_type

class Recapper:
    def __init__(self, fname):
        if not os.path.exists(fname):
            print(f"[-] Error: PCAP file not found at {fname}")
            sys.exit(1)
        
        print(f"[*] Reading {fname}...")
        pcap = rdpcap(fname)
        self.sessions = pcap.sessions()
        self.responses = list()
        print(f"[*] Found {len(self.sessions)} sessions.")

    def get_responses(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:
                try:
                    if packet.haslayer(TCP) and packet.haslayer('Raw'):
                        payload += bytes(packet.getlayer('Raw').load)
                except Exception:
                    continue
        
            if payload:
                # We search for the HTTP OK marker anywhere in the stream
                if b'HTTP/1.1 200 OK' in payload:
                    # Trim to start at the response
                    payload = payload[payload.index(b'HTTP/1.1 200 OK'):]
                    
                    header = get_header(payload)
                    if header:
                        print(f" [+] Found {header.get('Content-Type')} ({len(payload)} bytes)")
                        self.responses.append(Response(header=header, payload=payload))
        
        print(f"\n[*] Total valid responses identified: {len(self.responses)}")

    def write(self, content_name):
        # Create directory if missing
        if not os.path.exists(OUTDIR):
            os.makedirs(OUTDIR, exist_ok=True)
            print(f"[*] Created directory: {OUTDIR}")

        for i, response in enumerate(self.responses):
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                with open(fname, 'wb') as f:
                    f.write(content)
                print(f" [!] SUCCESSFULLY WROTE: {fname}")

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'test_images.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')

