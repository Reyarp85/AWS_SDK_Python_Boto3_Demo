import boto3
import pprint


def detect_sentiment(text, language_code):
    comp = boto3.client('comprehend')
    response = comp.detect_sentiment(Text=text, LanguageCode=language_code)
    return response


def main():
    language_codes = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Simplified Chinese',
        'zh-TW': 'Traditional Chinese',
    }

    print("Available language codes:")
    for code, language in language_codes.items():
        print(f"{code}: {language}")

    while True:
        text = input("\nEnter the text to analyze (or type 'q' to quit): ")
        if text.lower() == 'q':
            break
        language_code = input("Enter the language code: ")
        if language_code not in language_codes:
            print("Invalid language code. Please try again.")
            continue
        sentiment_response = detect_sentiment(text, language_code)
        pprint.pprint(sentiment_response)


if __name__ == '__main__':
    main()
