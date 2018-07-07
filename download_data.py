"""Download data relevant to train the KittiSeg model."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import sys
import os
import subprocess

import zipfile
from google_drive_downloader import GoogleDriveDownloader as gdd


from six.moves import urllib
from shutil import copy2

import argparse

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

sys.path.insert(1, 'incl')

# Please set kitti_data_url to the download link for the Kitti DATA.
#
# You can obtain by going to this website:
# http://www.cvlibs.net/download.php?file=data_road.zip
#
# Replace 'http://kitti.is.tue.mpg.de/kitti/?????????.???' by the
# correct URL.


#vgg_data_url = 'ftp://mi.eng.cam.ac.uk/pub/mttt2/models/vgg16.npy'


def download(url, dest_directory):
    filename = url.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    
    logging.info("Download URL: {}".format(url))
    logging.info("Download DIR: {}".format(dest_directory))
    
    def _progress(count, block_size, total_size):
        prog = float(count * block_size) / float(total_size) * 100.0
        sys.stdout.write('\r>> Downloading %s %.1f%%' %
                         (filename, prog))
        sys.stdout.flush()
    
    filepath, _ = urllib.request.urlretrieve(url, filepath,
                                             reporthook=_progress)
    print('')
    return filepath


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',
                        default='./data',
                        type=str)
    # https://drive.google.com/file/d/0B-Eiyn-CUQtxdUZWMkFfQzdObUE/view
    parser.add_argument('--dataset',
                        default='0B-Eiyn-CUQtxdUZWMkFfQzdObUE',
                        type=str)
    args = parser.parse_args()
    
    dataset_id = args.dataset
    data_dir = args.data_dir
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    dataset_zip = os.path.join(data_dir, 'dataset-sdcnd-capstone.zip')

    if not os.path.exists(dataset_zip):
        logging.info("Downloading dataset-sdcnd-capstone.")
        # Download files from Google Drive
        gdd.download_file_from_google_drive(file_id=dataset_id, dest_path=dataset_zip, unzip=True)

    logging.info("All data have been downloaded successful.")


if __name__ == '__main__':
    main()

