import aiohttp
import asyncio
import re

class Posts():
    def __init__(self):
        super().__init__()

    async def fetch_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"API 요청에 실패했습니다. 상태 코드: {response.status}")
                    return None

    async def extract_threads(self, data, threads_name):
        if data:
            threads = data.get(threads_name, [])
            filtered_data = []
            for thread in threads:
                thread['title'] = thread['title'].replace('&amp;', '&')

                filtered_data.append({
                    'threadId': thread['threadId'],
                    'boardId': thread['boardId'],
                    'title': thread['title'],
                    'createDate': thread['createDate']
                })
            return filtered_data

    # 업데이트상세, 이미지 URL 추출
    async def get_images(self):
        # API URL
        api_url = "https://forum.nexon.com/api/v1/board/1076/threads?alias=bluearchive&pageNo=1&paginationType=PAGING&pageSize=1&hideType=WEB&searchKeywordType=THREAD_TITLE&keywords=상세"
        # API 요청 보내기
        data = await self.fetch_data(api_url)
        if data:
            thread_id = data["threads"][0]["threadId"]
            board_id = data["threads"][0]["boardId"]
            api_url = f"https://forum.nexon.com/api/v1/thread/{thread_id}?alias=bluearchive"
            api_url_update = f"https://forum.nexon.com/bluearchive/board_view?board={board_id}&thread={thread_id}"
            image_width = 780
            image_height = 439
            data = await self.fetch_data(api_url)
            if data:
                pattern = rf'<img[^>]*?\s*src="([^"]+)"[^>]*?\s*style="[^"]*?\bwidth:\s*{image_width}px;[^"]*?\bheight:\s*{image_height}px;[^"]*?"[^>]*?>'
                image_urls = re.findall(pattern, data["content"])
                return api_url_update, image_urls

    # 주요소식 URL 추출
    async def get_maintopic(self):
        # API 엔드포인트 URL
        api_url = "https://forum.nexon.com/api/v1/community/148/stickyThreads?alias=bluearchive&pageSize=20&hideType=WEB"
        data = await self.fetch_data(api_url)
        return await self.extract_threads(data,'stickyThreads')

    # 공지사항 URL 추출
    async def get_notice(self):
        # API 엔드포인트 URL
        api_url = "https://forum.nexon.com/api/v1/board/1018/threads?alias=bluearchive&paginationType=PAGING&pageSize=15&pageNo=1&blockSize=5&hideType=WEB"
        data = await self.fetch_data(api_url)
        return await self.extract_threads(data,'threads')
    
async def main():
    posts = Posts()
    images = await posts.get_images()
    maintopics = await posts.get_maintopic()
    notices = await posts.get_notice()
    
if __name__ == "__main__":
    asyncio.run(main())    