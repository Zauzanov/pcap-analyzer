from scapy.all import TCP, rdpcap
import collections
import os
import re
import sys
import zlib

OUTDIR = '/home/kali/Desktop/pictures'
PCAPS = '/home/kali/Downloads'

Response = collections.namedtuple('Response', ['header', 'payload'])

def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None 
    
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

