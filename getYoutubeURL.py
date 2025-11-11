"""
YouTube 播放清單影片網址擷取器
使用 yt-dlp 套件 (不需要 API 金鑰)

安裝方法:
pip install yt-dlp
"""

import yt_dlp
import sys


def get_playlist_videos(playlist_url):
    """
    取得 YouTube 播放清單中所有影片的網址
    
    參數:
        playlist_url: YouTube 播放清單網址或 ID
    
    回傳:
        影片網址列表
    """
    # 如果只輸入 ID,組成完整網址
    if not playlist_url.startswith('http'):
        playlist_url = f'https://www.youtube.com/playlist?list={playlist_url}'
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }
    
    video_urls = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print('正在取得播放清單資訊...')
            info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        video_id = entry.get('id')
                        if video_id:
                            video_url = f'https://www.youtube.com/watch?v={video_id}'
                            video_urls.append(video_url)
        
        return video_urls
    
    except Exception as e:
        print(f'發生錯誤: {e}')
        return []


# 主程式
if __name__ == '__main__':
    print('YouTube 播放清單影片網址擷取器')
    print('=' * 50)
    
    # 輸入播放清單網址或 ID
    playlist_input = input('\n請輸入 YouTube 播放清單網址或 ID: ').strip()
    
    if not playlist_input:
        print("錯誤: 未輸入播放清單網址!")
        sys.exit(1)
    
    print()
    
    # 取得所有影片網址
    videos = get_playlist_videos(playlist_input)
    
    # 顯示結果
    if videos:
        print(f'\n✓ 成功! 找到 {len(videos)} 個影片:\n')
        print('=' * 50)
        for url in videos:
            print(f'{url}')
        print('=' * 50)
        
        # 詢問是否儲存到檔案
        save = input('\n是否要將網址儲存到檔案? (y/n): ').strip().lower()
        if save == 'y':
            filename = input('請輸入檔案名稱 (預設: playlist_videos.txt): ').strip()
            if not filename:
                filename = 'playlist_videos.txt'
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for url in videos:
                        f.write(url + '\n')
                print(f'\n✓ 已儲存到 {filename}')
            except Exception as e:
                print(f'\n✗ 儲存失敗: {e}')
    else:
        print('\n✗ 未找到影片或發生錯誤')
        sys.exit(1)