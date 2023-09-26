from simple_image_download import simple_image_download as downloader


def download_img():
    img_downloader = downloader.simple_image_download

    keywords = input("Enter image to download :: ")
    count = int(input("Number of images :: "))

    img_downloader().download(keywords, count)


if __name__ == "__main__":
    download_img()
