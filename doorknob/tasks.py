from rekognition import VideoDetect
from score import score

def start_watching(file_url):
    analyzer = VideoDetect(file_url)
    analyzer.CreateTopicandQueue()
    analyzer.main()
    analyzer.DeleteTopicandQueue()
    return score(analyzer.ratings)

if __name__ == "__main__":
    print("Score:", start_watching("emotion-test/Screen Recording 2020-06-28 at 12.52.49 PM.mov"))
