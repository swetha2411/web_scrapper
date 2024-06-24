from requests_html import HTMLSession
import json
import time

class Reviews:
    def __init__(self, asin) -> None:
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
        self.url = f'https://www.amazon.in/Intel-Generation-Processor-Warranty-Required/product-reviews/{self.asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='

    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        r.html.render()  # Render the JavaScript on the page (this can take a few seconds)
        print(r.html.html)  # Print the entire HTML content for debugging
        if not r.html.find('div[data-hook=review]'):
            return False
        else:
            return r.html.find('div[data-hook=review]')

    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('span[data-hook=review-title] span', first=True)
            rating = review.find('i[data-hook=cmps-review-star-rating] span', first=True)
            body = review.find('span[data-hook=review-body] span', first=True)

            if title is None or rating is None or body is None:
                print("Missing element in review, skipping...")
                continue

            data = {
                'title': title.text if title else 'No Title',
                'rating': rating.text if rating else 'No Rating',
                'body': body.text.replace('\n', '').strip()[:100] if body else 'No Body'
            }
            total.append(data)
        return total

    def save(self, results):
        with open(self.asin + '-reviews.json', 'w') as f:
            json.dump(results, f)

if __name__ == '__main__':
    amz = Reviews('B09MDJDSGH')
    results = []
    for x in range(2,11):
        print('getting page',x)
        time.sleep(0.3)
        reviews = amz.pagination(x)
        if reviews:
            parsed_reviews = amz.parse(reviews)
            results.extend(parsed_reviews)
        else:
            print('No more pages')
            break
    amz.save(results)


