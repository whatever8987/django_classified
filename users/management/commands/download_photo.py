import requests
from bs4 import BeautifulSoup
import urllib3
import json
import psycopg2
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from django.core.management.base import BaseCommand
import random
import string

# Suppress only the single InsecureRequestWarning from urllib3 needed for requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Define specific URLs to exclude
exclude_urls = ["/static/images/phone.png", "/static/images/pin.png", "/ad/238319.html"]
data = []

# Function to generate a random string
def random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Function to download images
def download_image(url, folder, file_name):
    try:
        # Send a HTTP request to the URL with SSL verification disabled
        response = requests.get(url, verify=False)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Ensure the folder exists
            os.makedirs(folder, exist_ok=True)
            # Append a random string to the filename to ensure uniqueness
            unique_file_name = f"{os.path.splitext(file_name)[0]}_{random_string()}{os.path.splitext(file_name)[1]}"
            # Create the full file path
            file_path = os.path.join(folder, unique_file_name)
            # Open a local file with the specified name in binary write mode
            with open(file_path, 'wb') as file:
                # Write the content of the response (image) to the file
                file.write(response.content)
            print(f"Image successfully downloaded: {file_path}")
            return unique_file_name  # Return only the unique file name
        else:
            print(f"Failed to retrieve the image from {url}. HTTP Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")
        return None

base_url = 'https://bodyrubsmap.com'
urls = [   
f'{base_url}/city/390.html',
#f'{base_url}/city/391.html',
#f'{base_url}/city/392.html',
#f'{base_url}/city/393.html',
#f'{base_url}/city/394.html',
#f'{base_url}/city/395.html',
#f'{base_url}/city/396.html',
#f'{base_url}/city/397.html',
#f'{base_url}/city/398.html',
#f'{base_url}/city/446.html',
#f'{base_url}/city/327.html',
#f'{base_url}/city/328.html',
#f'{base_url}/city/329.html',
#f'{base_url}/city/330.html',
#f'{base_url}/city/250.html',
#f'{base_url}/city/457.html',
#f'{base_url}/city/251.html',
#f'{base_url}/city/252.html',
#f'{base_url}/city/253.html',
#f'{base_url}/city/254.html',
#f'{base_url}/city/255.html',
#f'{base_url}/city/256.html',
#f'{base_url}/city/257.html',
#f'{base_url}/city/351.html',
#f'{base_url}/city/352.html',
#f'{base_url}/city/353.html',
#f'{base_url}/city/354.html',
#f'{base_url}/city/186.html',
#f'{base_url}/city/187.html',
#f'{base_url}/city/434.html',
#f'{base_url}/city/188.html',
#f'{base_url}/city/189.html',
#f'{base_url}/city/190.html',
#f'{base_url}/city/191.html',
#f'{base_url}/city/433.html',
#f'{base_url}/city/192.html',
#f'{base_url}/city/193.html',
#f'{base_url}/city/477.html',
#f'{base_url}/city/194.html',
#f'{base_url}/city/195.html',
#f'{base_url}/city/196.html',
#f'{base_url}/city/197.html',
#f'{base_url}/city/198.html',
#f'{base_url}/city/199.html',
#f'{base_url}/city/200.html',
#f'{base_url}/city/201.html',
#f'{base_url}/city/202.html',
#f'{base_url}/city/203.html',
#f'{base_url}/city/204.html',
#f'{base_url}/city/205.html',
#f'{base_url}/city/206.html',
#f'{base_url}/city/207.html',
#f'{base_url}/city/208.html',
#f'{base_url}/city/209.html',
#f'{base_url}/city/210.html',
#f'{base_url}/city/211.html',
#f'{base_url}/city/495.html',
#f'{base_url}/city/212.html',
#f'{base_url}/city/213.html',
#f'{base_url}/city/214.html',
#f'{base_url}/city/215.html',
#f'{base_url}/city/216.html',
#f'{base_url}/city/217.html',
#f'{base_url}/city/480.html',
#f'{base_url}/city/432.html',
#f'{base_url}/city/218.html',
#f'{base_url}/city/219.html',
#f'{base_url}/city/320.html',
#f'{base_url}/city/321.html',
#f'{base_url}/city/322.html',
#f'{base_url}/city/323.html',
#f'{base_url}/city/324.html',
#f'{base_url}/city/325.html',
#f'{base_url}/city/326.html',
#f'{base_url}/city/83.html',
#f'{base_url}/city/88.html',
#f'{base_url}/city/84.html',
#f'{base_url}/city/85.html',
#f'{base_url}/city/500.html',
#f'{base_url}/city/86.html',
#f'{base_url}/city/87.html',
#f'{base_url}/city/460.html',
#f'{base_url}/city/493.html',
#f'{base_url}/city/469.html',
#f'{base_url}/city/369.html',
#f'{base_url}/city/471.html',
#f'{base_url}/city/370.html',
#f'{base_url}/city/371.html',
#f'{base_url}/city/372.html',
#f'{base_url}/city/373.html',
#f'{base_url}/city/374.html',
#f'{base_url}/city/375.html',
#f'{base_url}/city/489.html',
#f'{base_url}/city/376.html',
#f'{base_url}/city/503.html',
#f'{base_url}/city/377.html',
#f'{base_url}/city/378.html',
#f'{base_url}/city/379.html',
#f'{base_url}/city/380.html',
#f'{base_url}/city/381.html',
#f'{base_url}/city/382.html',
#f'{base_url}/city/383.html',
#f'{base_url}/city/384.html',
#f'{base_url}/city/385.html',
#f'{base_url}/city/386.html',
#f'{base_url}/city/387.html',
#f'{base_url}/city/388.html',
#f'{base_url}/city/389.html',
#f'{base_url}/city/331.html',
#f'{base_url}/city/332.html',
#f'{base_url}/city/333.html',
#f'{base_url}/city/334.html',
#f'{base_url}/city/335.html',
#f'{base_url}/city/336.html',
#f'{base_url}/city/337.html',
#f'{base_url}/city/498.html',
#f'{base_url}/city/338.html',
#f'{base_url}/city/339.html',
#f'{base_url}/city/340.html',
#f'{base_url}/city/341.html',
#f'{base_url}/city/225.html',
#f'{base_url}/city/226.html',
#f'{base_url}/city/227.html',
#f'{base_url}/city/228.html',
#f'{base_url}/city/273.html',
#f'{base_url}/city/274.html',
#f'{base_url}/city/275.html',
#f'{base_url}/city/276.html',
#f'{base_url}/city/461.html',
#f'{base_url}/city/104.html',
#f'{base_url}/city/105.html',
#f'{base_url}/city/106.html',
#f'{base_url}/city/107.html',
#f'{base_url}/city/497.html',
#f'{base_url}/city/108.html',
#f'{base_url}/city/481.html',
#f'{base_url}/city/482.html',
#f'{base_url}/city/109.html',
#f'{base_url}/city/110.html',
#f'{base_url}/city/111.html',
#f'{base_url}/city/112.html',
#f'{base_url}/city/113.html',
#f'{base_url}/city/114.html',
#f'{base_url}/city/465.html',
#f'{base_url}/city/58.html',
#f'{base_url}/city/59.html',
#f'{base_url}/city/60.html',
#f'{base_url}/city/61.html',
#f'{base_url}/city/62.html',
#f'{base_url}/city/63.html',
#f'{base_url}/city/64.html',
#f'{base_url}/city/65.html',
#f'{base_url}/city/66.html',
#f'{base_url}/city/67.html',
#f'{base_url}/city/93.html',
#f'{base_url}/city/94.html',
#f'{base_url}/city/95.html',
#f'{base_url}/city/96.html',
#f'{base_url}/city/97.html',
#f'{base_url}/city/98.html',
#f'{base_url}/city/99.html',
#f'{base_url}/city/501.html',
#f'{base_url}/city/100.html',
#f'{base_url}/city/101.html',
#f'{base_url}/city/102.html',
#f'{base_url}/city/103.html',
#f'{base_url}/city/496.html',
#f'{base_url}/city/220.html',
#f'{base_url}/city/221.html',
#f'{base_url}/city/222.html',
#f'{base_url}/city/223.html',
#f'{base_url}/city/224.html',
#f'{base_url}/city/363.html',
#f'{base_url}/city/364.html',
#f'{base_url}/city/463.html',
#f'{base_url}/city/365.html',
#f'{base_url}/city/366.html',
#f'{base_url}/city/367.html',
#f'{base_url}/city/368.html',
#f'{base_url}/city/423.html',
#f'{base_url}/city/424.html',
#f'{base_url}/city/435.html',
#f'{base_url}/city/504.html',
#f'{base_url}/city/449.html',
#f'{base_url}/city/425.html',
#f'{base_url}/city/426.html',
#f'{base_url}/city/427.html',
#f'{base_url}/city/454.html',
#f'{base_url}/city/428.html',
#f'{base_url}/city/484.html',
#f'{base_url}/city/429.html',
#f'{base_url}/city/430.html',
#f'{base_url}/city/508.html',
#f'{base_url}/city/444.html',
#f'{base_url}/city/42.html',
#f'{base_url}/city/43.html',
#f'{base_url}/city/44.html',
#f'{base_url}/city/45.html',
#f'{base_url}/city/46.html',
#f'{base_url}/city/487.html',
#f'{base_url}/city/47.html',
#f'{base_url}/city/133.html',
#f'{base_url}/city/134.html',
#f'{base_url}/city/135.html',
#f'{base_url}/city/488.html',
#f'{base_url}/city/136.html',
#f'{base_url}/city/451.html',
#f'{base_url}/city/137.html',
#f'{base_url}/city/138.html',
#f'{base_url}/city/139.html',
#f'{base_url}/city/153.html',
#f'{base_url}/city/154.html',
#f'{base_url}/city/155.html',
#f'{base_url}/city/486.html',
#f'{base_url}/city/156.html',
#f'{base_url}/city/157.html',
#f'{base_url}/city/158.html',
#f'{base_url}/city/159.html',
#f'{base_url}/city/160.html',
#f'{base_url}/city/161.html',
#f'{base_url}/city/162.html',
#f'{base_url}/city/163.html',
#f'{base_url}/city/164.html',
#f'{base_url}/city/165.html',
#f'{base_url}/city/436.html',
#f'{base_url}/city/166.html',
#f'{base_url}/city/167.html',
#f'{base_url}/city/499.html',
#f'{base_url}/city/168.html',
#f'{base_url}/city/169.html',
#f'{base_url}/city/448.html',
#f'{base_url}/city/68.html',
#f'{base_url}/city/69.html',
#f'{base_url}/city/70.html',
#f'{base_url}/city/71.html',
#f'{base_url}/city/72.html',
#f'{base_url}/city/445.html',
#f'{base_url}/city/73.html',
#f'{base_url}/city/74.html',
#f'{base_url}/city/442.html',
#f'{base_url}/city/459.html',
#f'{base_url}/city/478.html',
#f'{base_url}/city/399.html',
#f'{base_url}/city/400.html',
#f'{base_url}/city/401.html',
#f'{base_url}/city/402.html',
#f'{base_url}/city/403.html',
#f'{base_url}/city/404.html',
#f'{base_url}/city/342.html',
#f'{base_url}/city/343.html',
#f'{base_url}/city/344.html',
#f'{base_url}/city/345.html',
#f'{base_url}/city/346.html',
#f'{base_url}/city/347.html',
#f'{base_url}/city/348.html',
#f'{base_url}/city/349.html',
#f'{base_url}/city/350.html',
#f'{base_url}/city/233.html',
#f'{base_url}/city/234.html',
#f'{base_url}/city/235.html',
#f'{base_url}/city/236.html',
#f'{base_url}/city/237.html',
#f'{base_url}/city/238.html',
#f'{base_url}/city/239.html',
#f'{base_url}/city/263.html',
#f'{base_url}/city/264.html',
#f'{base_url}/city/265.html',
#f'{base_url}/city/266.html',
#f'{base_url}/city/267.html',
#f'{base_url}/city/277.html',
#f'{base_url}/city/278.html',
#f'{base_url}/city/279.html',
#f'{base_url}/city/490.html',
#f'{base_url}/city/505.html',
#f'{base_url}/city/89.html',
#f'{base_url}/city/90.html',
#f'{base_url}/city/91.html',
#f'{base_url}/city/92.html',
#f'{base_url}/city/244.html',
#f'{base_url}/city/245.html',
#f'{base_url}/city/246.html',
#f'{base_url}/city/247.html',
#f'{base_url}/city/248.html',
#f'{base_url}/city/249.html',
#f'{base_url}/city/1.html',
#f'{base_url}/city/2.html',
#f'{base_url}/city/3.html',
#f'{base_url}/city/4.html',
#f'{base_url}/city/5.html',
#f'{base_url}/city/464.html',
#f'{base_url}/city/6.html',
#f'{base_url}/city/7.html',
#f'{base_url}/city/8.html',
#f'{base_url}/city/9.html',
#f'{base_url}/city/10.html',
#f'{base_url}/city/441.html',
#f'{base_url}/city/11.html',
#f'{base_url}/city/12.html',
#f'{base_url}/city/13.html',
#f'{base_url}/city/14.html',
#f'{base_url}/city/15.html',
#f'{base_url}/city/16.html',
#f'{base_url}/city/17.html',
#f'{base_url}/city/472.html',
#f'{base_url}/city/18.html',
#f'{base_url}/city/19.html',
#f'{base_url}/city/20.html',
#f'{base_url}/city/21.html',
#f'{base_url}/city/22.html',
#f'{base_url}/city/23.html',
#f'{base_url}/city/24.html',
#f'{base_url}/city/25.html',
#f'{base_url}/city/26.html',
#f'{base_url}/city/405.html',
#f'{base_url}/city/406.html',
#f'{base_url}/city/407.html',
#f'{base_url}/city/408.html',
#f'{base_url}/city/409.html',
#f'{base_url}/city/410.html',
#f'{base_url}/city/411.html',
#f'{base_url}/city/412.html',
#f'{base_url}/city/413.html',
#f'{base_url}/city/414.html',
#f'{base_url}/city/415.html',
#f'{base_url}/city/416.html',
#f'{base_url}/city/229.html',
#f'{base_url}/city/230.html',
#f'{base_url}/city/231.html',
#f'{base_url}/city/232.html',
#f'{base_url}/city/170.html',
#f'{base_url}/city/171.html',
#f'{base_url}/city/172.html',
#f'{base_url}/city/173.html',
#f'{base_url}/city/174.html',
#f'{base_url}/city/175.html',
#f'{base_url}/city/176.html',
#f'{base_url}/city/177.html',
#f'{base_url}/city/178.html',
#f'{base_url}/city/483.html',
#f'{base_url}/city/179.html',
#f'{base_url}/city/180.html',
#f'{base_url}/city/181.html',
#f'{base_url}/city/182.html',
#f'{base_url}/city/183.html',
#f'{base_url}/city/184.html',
#f'{base_url}/city/185.html',
#f'{base_url}/city/258.html',
#f'{base_url}/city/259.html',
#f'{base_url}/city/260.html',
#f'{base_url}/city/261.html',
#f'{base_url}/city/262.html',
#f'{base_url}/city/450.html',
#f'{base_url}/city/280.html',
#f'{base_url}/city/281.html',
#f'{base_url}/city/282.html',
#f'{base_url}/city/283.html',
#f'{base_url}/city/284.html',
#f'{base_url}/city/285.html',
#f'{base_url}/city/286.html',
#f'{base_url}/city/287.html',
#f'{base_url}/city/288.html',
#f'{base_url}/city/289.html',
#f'{base_url}/city/467.html',
#f'{base_url}/city/439.html',
#f'{base_url}/city/27.html',
#f'{base_url}/city/28.html',
#f'{base_url}/city/437.html',
#f'{base_url}/city/29.html',
#f'{base_url}/city/30.html',
#f'{base_url}/city/31.html',
#f'{base_url}/city/32.html',
#f'{base_url}/city/33.html',
#f'{base_url}/city/34.html',
#f'{base_url}/city/35.html',
#f'{base_url}/city/36.html',
#f'{base_url}/city/37.html',
#f'{base_url}/city/38.html',
#f'{base_url}/city/39.html',
#f'{base_url}/city/440.html',
#f'{base_url}/city/40.html',
#f'{base_url}/city/41.html',
#f'{base_url}/city/115.html',
#f'{base_url}/city/116.html',
#f'{base_url}/city/417.html',
#f'{base_url}/city/418.html',
#f'{base_url}/city/419.html',
#f'{base_url}/city/420.html',
#f'{base_url}/city/421.html',
#f'{base_url}/city/422.html',
#f'{base_url}/city/240.html',
#f'{base_url}/city/241.html',
#f'{base_url}/city/242.html',
#f'{base_url}/city/243.html',
#f'{base_url}/city/355.html',
#f'{base_url}/city/356.html',
#f'{base_url}/city/357.html',
#f'{base_url}/city/358.html',
#f'{base_url}/city/359.html',
#f'{base_url}/city/360.html',
#f'{base_url}/city/361.html',
#f'{base_url}/city/362.html',
#f'{base_url}/city/290.html',
#f'{base_url}/city/291.html',
#f'{base_url}/city/292.html',
#f'{base_url}/city/293.html',
#f'{base_url}/city/294.html',
#f'{base_url}/city/452.html',
#f'{base_url}/city/295.html',
#f'{base_url}/city/296.html',
#f'{base_url}/city/297.html',
#f'{base_url}/city/298.html',
#f'{base_url}/city/299.html',
#f'{base_url}/city/300.html',
#f'{base_url}/city/301.html',
#f'{base_url}/city/302.html',
#f'{base_url}/city/466.html',
#f'{base_url}/city/303.html',
#f'{base_url}/city/304.html',
#f'{base_url}/city/476.html',
#f'{base_url}/city/305.html',
#f'{base_url}/city/306.html',
#f'{base_url}/city/307.html',
#f'{base_url}/city/308.html',
#f'{base_url}/city/462.html',
#f'{base_url}/city/309.html',
#f'{base_url}/city/310.html',
#f'{base_url}/city/470.html',
#f'{base_url}/city/311.html',
#f'{base_url}/city/453.html',
#f'{base_url}/city/312.html',
#f'{base_url}/city/313.html',
#f'{base_url}/city/455.html',
#f'{base_url}/city/314.html',
#f'{base_url}/city/315.html',
#f'{base_url}/city/316.html',
#f'{base_url}/city/317.html',
#f'{base_url}/city/318.html',
#f'{base_url}/city/319.html',
#f'{base_url}/city/268.html',
#f'{base_url}/city/269.html',
#f'{base_url}/city/270.html',
#f'{base_url}/city/271.html',
#f'{base_url}/city/272.html',
#f'{base_url}/city/507.html',
#f'{base_url}/city/494.html',
#f'{base_url}/city/117.html',
#f'{base_url}/city/118.html',
#f'{base_url}/city/119.html',
#f'{base_url}/city/491.html',
#f'{base_url}/city/120.html',
#f'{base_url}/city/468.html',
#f'{base_url}/city/121.html',
#f'{base_url}/city/122.html',
#f'{base_url}/city/123.html',
#f'{base_url}/city/475.html',
#f'{base_url}/city/124.html',
#f'{base_url}/city/125.html',
#f'{base_url}/city/126.html',
#f'{base_url}/city/127.html',
#f'{base_url}/city/128.html',
#f'{base_url}/city/129.html',
#f'{base_url}/city/130.html',
#f'{base_url}/city/131.html',
#f'{base_url}/city/132.html',
#f'{base_url}/city/485.html',
#f'{base_url}/city/140.html',
#f'{base_url}/city/458.html',
#f'{base_url}/city/148.html',
#f'{base_url}/city/141.html',
#f'{base_url}/city/492.html',
#f'{base_url}/city/438.html',
#f'{base_url}/city/443.html',
#f'{base_url}/city/447.html',
#f'{base_url}/city/142.html',
#f'{base_url}/city/143.html',
#f'{base_url}/city/144.html',
#f'{base_url}/city/145.html',
#f'{base_url}/city/146.html',
#f'{base_url}/city/147.html',
#f'{base_url}/city/149.html',
#f'{base_url}/city/150.html',
#f'{base_url}/city/431.html',
#f'{base_url}/city/151.html',
#f'{base_url}/city/152.html',
#f'{base_url}/city/474.html',
#f'{base_url}/city/502.html',
#f'{base_url}/city/75.html',
#f'{base_url}/city/76.html',
#f'{base_url}/city/77.html',
#f'{base_url}/city/78.html',
#f'{base_url}/city/79.html',
#f'{base_url}/city/80.html',
#f'{base_url}/city/81.html',
#f'{base_url}/city/82.html',
#f'{base_url}/city/48.html',
#f'{base_url}/city/49.html',
#f'{base_url}/city/456.html',
#f'{base_url}/city/50.html',
#f'{base_url}/city/51.html',
#f'{base_url}/city/52.html',
#f'{base_url}/city/53.html',
#f'{base_url}/city/54.html',
#f'{base_url}/city/55.html',
#f'{base_url}/city/56.html',
#f'{base_url}/city/57.html',
#f'{base_url}/city/473.html',
#f'{base_url}/city/506.html',
]

class Command(BaseCommand):
    help = 'Scrape and download images, then insert data into the PostgreSQL database'

    def handle(self, *args, **kwargs):
        # Loop through each URL in the list
        for url in urls:
            # Send a GET request to the website with SSL verification disabled
            response = requests.get(url, verify=False)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all <a> elements with class 'ad-link'
                ad_links = soup.find_all('a', class_='ad-link')

                for link_text, link in enumerate(ad_links, start=1):  # Adjust start index as needed
                    href = link.get('href')
                    
                    # Check if href is in exclude_urls, skip if true
                    if any(exclude_url in href for exclude_url in exclude_urls):
                        continue
                    
                    # Simulate clicking the link by sending a GET request to the href
                    full_url = requests.compat.urljoin(base_url, href)
                    ad_response = requests.get(full_url, verify=False)
                    
                    if ad_response.status_code == 200:
                        # Parse the HTML content of the linked page
                        ad_soup = BeautifulSoup(ad_response.content, 'html.parser')
                        
                        # Find all <img> elements and extract their src attribute
                        images = ad_soup.find_all('img')
                        img_srcs = [
                            base_url + img.get('src') if img.get('src').startswith('/') else img.get('src')
                            for img in images
                            if img.get('src') and not any(exclude_url in img.get('src') for exclude_url in exclude_urls)
                        ]
                        
                        # Download images and get their local file names
                        download_img_paths = []
                        for index, img_url in enumerate(img_srcs):
                            file_name = f'download_image_{link_text}_{index + 1}.jpg'
                            file_name_only = os.path.basename(file_name)  # Get only the file name
                            file_path = download_image(img_url, 'media/images', file_name)
                            if file_path:
                                download_img_paths.append(file_path)  # Append only the unique file name
                        
                        # Add link_text and download image file names to the data list as a dictionary
                        data.append({"item_id": str(link_text), "file": download_img_paths})
                        
                        # Print link_text (item_id) and download image file names
                        print(f'Processed link: {link_text}, Images: {download_img_paths}')
                    
                    else:
                        print(f'Failed to process link: {link_text}, URL: {full_url}')
            
            else:
                print(f'Failed to retrieve the webpage: {url}')

        # Save the data to a JSON file
        with open('scraped_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print('Data saved to scraped_data.json')

        # Function to insert data into the PostgreSQL database
        def insert_data_to_db(data):
            try:
                import psycopg2
                
                # Establish a connection to the PostgreSQL database
                conn = psycopg2.connect(
                    dbname="kiemthatnhieutien",
                    user="master",
                    password="master",
                    host="localhost",
                    port="5432"
                )
                
                # Create a cursor object
                cursor = conn.cursor()
                
                # Define the insert query
                insert_query = """
                INSERT INTO django_classified_image (item_id, file)
                VALUES (%s, %s)
                """
                
                # Insert each item in the data list
                for item in data:
                    cursor.execute(insert_query, (item['item_id'], json.dumps(item['file'])))
                
                # Commit the transaction
                conn.commit()
                
                # Close the cursor and connection
                cursor.close()
                conn.close()
                
                print("Data inserted successfully")
                
            except Exception as e:
                print(f"Error inserting data into the database: {e}")

        # Load the scraped data from the JSON file
        with open('scraped_data.json', 'r') as json_file:
            scraped_data = json.load(json_file)

        # Insert the scraped data into the PostgreSQL database
        insert_data_to_db(scraped_data)
