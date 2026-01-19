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