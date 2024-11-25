from youtube_transcript_api import YouTubeTranscriptApi
from utils.transcript import split_transcript_into_chunks, summarize_chunk

def get_content_origin():
    while True:
        origin = input("What is the origin of the content? ").lower()
        if origin == "youtube":
            return origin
        else:
            print("Origin not supported.")

def get_youtube_transcript():
    youtube_id = input("Please enter the YouTube video ID (part after 'v=' in the URL): ")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(youtube_id)
        full_transcript = " ".join(entry['text'] for entry in transcript)
        
        chunks = split_transcript_into_chunks(full_transcript, chunk_size=2000, chunk_overlap=300)
        
        for i, chunk in enumerate(chunks, 1):
            print(f"\nChunk {i}:")
            print(chunk.page_content)
            print("\nSummary:")
            result = summarize_chunk(chunk.page_content)
            print(f"Summary: {result.summary}")
            print(f"Important: {result.isImportant}")
            print("-" * 80)

    except Exception as e:
        print(f"Error: {e}")

def main():
    origin = get_content_origin()
    
    if origin == "youtube":
        get_youtube_transcript()

if __name__ == "__main__":
    main()
