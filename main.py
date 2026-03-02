import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch(headless=False) as browser:
            async with await browser.new_context() as context:
                async with await context.new_page() as page:
                    urls = []
                    page.on("request", lambda request: urls.append(request.url))

                    await page.goto("https://www.news.cn/")

                    with open("urls.txt", "w") as file:
                        file.write(f"{len(urls)}\n")
                        for url in urls:
                            file.write(url + "\n")

                    hrefs_1 = await page.evaluate(
                        "()=>[...document.links].map(a=>a.href)"
                    )
                    with open("hrefs_1.txt", "w") as file:
                        file.write(f"{len(hrefs_1)}\n")
                        for href in hrefs_1:
                            file.write(href + "\n")

                    hrefs_2 = await page.evaluate(
                        "Array.from(document.querySelectorAll('a')).map(a=>a.href)"
                    )
                    with open("hrefs_2.txt", "w") as file:
                        file.write(f"{len(hrefs_2)}\n")
                        for href in hrefs_2:
                            file.write(href + "\n")


if __name__ == "__main__":
    asyncio.run(main())
