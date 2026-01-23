# pcap-analyzer

<p align="center">
  <h1 align="center"> an educational/research pcap files analyzer </h1>
	<p align="center">For cybersecurity professionals and educational purposes only!</p>
	<p align="center">Use only on hosts/networks you own or have permission to test!</p>
</p>

A Python-based pcap files analyzer that intercepts network traffic using Scapy and identifies human faces in captured images via OpenCV.

## 1. Preparations on Kali:
### 1.1 Install OpenCV libs:
```bash
sudo apt update
sudo apt-get install libopencv-dev python3-opencv python3-numpy python3-scipy
```
### 1.2 Download a pre-trained machine learning model provided by OpenCV used for detecting frontal faces in images or video streams. It is a Haar cascade classifier based on the Viola-Jones object detection framework, which identifies facial features by analyzing intensities of pixel groups:
```bash
wget https://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml
# or
wget https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_alt.xml
```
#### Or on Kali, OpenCV cascades are often pre-installed here:
```bash
/usr/share/opencv4/haarcascades
```
### 1.3 Create 3 folders on Desktop: 
```markdown
faces - for final result; 
training - for pre-trained OpenCV file. On Kali it's pre-installed and lives here: '/usr/share/opencv4/haarcascades'; 
pictures - for extracted images from .pcap file.
```
## 2. Generate .pcap file(you can also do it manually using Wireshark and browser) using my MockPacket tool:
```bash
sudo python3 generator.py
[sudo] password for kali: 
Downloading images and building packets...
 [+] Added face.jpg (30215 bytes)
 [+] Added nature.jpg (13489 bytes)
 [+] Added car.jpg (14077 bytes)
 [+] Added dog.jpg (31048 bytes)
 [+] Added fruit.jpg (26855 bytes)

Success! Generated 'test_images.pcap' with 5 images.
```

## 3. Sniff for images:
```bash
sudo python recapper.py
[*] Reading /home/kali/Downloads/test_images.pcap...
[*] Found 5 sessions.
 [+] Found image/jpeg (30302 bytes)
 [+] Found image/jpeg (13576 bytes)
 [+] Found image/jpeg (14164 bytes)
 [+] Found image/jpeg (31135 bytes)
 [+] Found image/jpeg (26942 bytes)

[*] Total valid responses identified: 5
 [!] SUCCESSFULLY WROTE: /home/kali/Desktop/pictures/ex_0.jpeg
 [!] SUCCESSFULLY WROTE: /home/kali/Desktop/pictures/ex_1.jpeg
 [!] SUCCESSFULLY WROTE: /home/kali/Desktop/pictures/ex_2.jpeg
 [!] SUCCESSFULLY WROTE: /home/kali/Desktop/pictures/ex_3.jpeg
 [!] SUCCESSFULLY WROTE: /home/kali/Desktop/pictures/ex_4.jpeg
```

### Check the extracted images:
![images](https://raw.githubusercontent.com/Zauzanov/pcap-analyzer/refs/heads/main/s01.png)


## 4. Detect faces in the newfound images:
```bash
python detector.py      
[*] Scanning /home/kali/Desktop/pictures for faces...
 [+] Found face in ex_0.jpeg!
[*] Detection complete. Found 1 faces.
```                                
### Check the result:
![face](https://raw.githubusercontent.com/Zauzanov/pcap-analyzer/refs/heads/main/s02.png)
