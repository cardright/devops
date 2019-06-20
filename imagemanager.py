import requests
import boto3
from tempfile import TemporaryFile
from flickrapi import FlickrAPI


class ImageManager:
    API_KEY = '012345678901234567890123456789af'
    SHARED_SECRET = '0123456789554a3f'

    report = ''

    def __init__(self):
        pass

    def download(self, search_term):
        flickr = FlickrAPI(self.API_KEY, self.SHARED_SECRET, format='parsed-json')
        list = flickr.photos.search(text=search_term, per_page=5, extras='url_m')
        photos = list['photos']
        for photo in photos['photo']:
            if 'url_m' not in photo:
                continue
            url = photo['url_m']
            tfile = TemporaryFile()
            req = requests.get(url, stream=True)
            with tfile:
                tfile.write(req.content)
                tfile.seek(0)
                client = boto3.client('rekognition')
                response = client.detect_labels(Image={'Bytes': tfile.read()}, MinConfidence=50)
            self.report = self.generate_report(photo['title'], response['Labels'], url)
        self.report += "</body></html>"
        with open('report.html', 'w') as report_html:
            report_html.write(self.report)

    def generate_report(self, title, labels, url):
        if not self.report:
            self.report = "<html><body>"
        label_names = list()
        for l in labels:
            label_names.append(l['Name'])

        self.report += "<div><span><b>Title:</b>" + title + "</span></div>\n"
        self.report += "<div><span><b>Detected:</b>" + ','.join(label_names) + "</span></div>\n"
        self.report += "<div><img src=\"" + url + "\"/></div>\n"
        self.report += "<br/>\n"
        self.report += "</div>\n"
        return self.report


