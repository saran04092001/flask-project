import re
from collections import Counter
import os
from datetime import datetime

class TextFileParser:
    def __init__(self):
        self.file_content = ""
        self.analysis_results = {}
        
    def load_file(self, file_path):
        """Load text content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.file_content = file.read()
            self.analysis_results['file_name'] = os.path.basename(file_path)
            self.analysis_results['load_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def basic_statistics(self):
        """Calculate basic text statistics"""
        if not self.file_content:
            return False
            
        words = re.findall(r'\w+', self.file_content.lower())
        sentences = re.split(r'[.!?]+', self.file_content)
        paragraphs = [p for p in self.file_content.split('\n\n') if p.strip()]
        
        self.analysis_results['statistics'] = {
            'char_count': len(self.file_content),
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len(paragraphs),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len([s for s in sentences if s.strip()]) if sentences else 0
        }
        return True
    
    def word_frequency(self, top_n=10):
        """Calculate word frequency"""
        if not self.file_content:
            return False
            
        words = re.findall(r'\w+', self.file_content.lower())
        word_counts = Counter(words)
        self.analysis_results['word_frequency'] = {
            'top_words': word_counts.most_common(top_n),
            'unique_words': len(word_counts)
        }
        return True
    
    def find_pattern(self, pattern):
        """Find all occurrences of a regex pattern"""
        if not self.file_content:
            return False
            
        matches = re.findall(pattern, self.file_content, re.IGNORECASE)
        self.analysis_results['pattern_matches'] = {
            'pattern': pattern,
            'matches': matches,
            'count': len(matches)
        }
        return True
    
    def extract_emails(self):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return self.find_pattern(email_pattern)
    
    def extract_urls(self):
        """Extract URLs from text"""
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*/?'
        return self.find_pattern(url_pattern)
    
    def analyze(self, file_path):
        """Run complete analysis on a file"""
        if not self.load_file(file_path):
            return None
            
        self.basic_statistics()
        self.word_frequency()
        self.extract_emails()
        self.extract_urls()
        
        return self.analysis_results
    
    def save_results(self, output_file):
        """Save analysis results to a file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write("Text File Analysis Report\n")
                file.write("="*40 + "\n")
                file.write(f"File: {self.analysis_results.get('file_name', 'N/A')}\n")
                file.write(f"Analyzed at: {self.analysis_results.get('load_time', 'N/A')}\n\n")
                
                stats = self.analysis_results.get('statistics', {})
                file.write("Basic Statistics:\n")
                file.write(f"- Characters: {stats.get('char_count', 0)}\n")
                file.write(f"- Words: {stats.get('word_count', 0)}\n")
                file.write(f"- Sentences: {stats.get('sentence_count', 0)}\n")
                file.write(f"- Paragraphs: {stats.get('paragraph_count', 0)}\n")
                file.write(f"- Avg word length: {stats.get('avg_word_length', 0):.2f}\n")
                file.write(f"- Avg sentence length: {stats.get('avg_sentence_length', 0):.2f} words\n\n")
                
                freq = self.analysis_results.get('word_frequency', {})
                file.write("Word Frequency:\n")
                file.write(f"- Unique words: {freq.get('unique_words', 0)}\n")
                file.write("- Top 10 words:\n")
                for word, count in freq.get('top_words', []):
                    file.write(f"  {word}: {count}\n")
                file.write("\n")
                
                emails = self.analysis_results.get('pattern_matches', {})
                if emails.get('pattern', '').endswith('@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'):
                    file.write(f"Email addresses found: {emails.get('count', 0)}\n")
                    for email in emails.get('matches', [])[:5]:  # Show first 5
                        file.write(f"- {email}\n")
                    if emails.get('count', 0) > 5:
                        file.write(f"- ... and {emails.get('count', 0)-5} more\n")
                    file.write("\n")
                
                urls = self.analysis_results.get('pattern_matches', {})
                if 'http' in urls.get('pattern', ''):
                    file.write(f"URLs found: {urls.get('count', 0)}\n")
                    for url in urls.get('matches', [])[:3]:  # Show first 3
                        file.write(f"- {url}\n")
                    if urls.get('count', 0) > 3:
                        file.write(f"- ... and {urls.get('count', 0)-3} more\n")
                
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False

def create_sample_input(file_path):
    """Create a sample input file for testing"""
    sample_text = """This is a sample text file for testing the AI text parser.

The parser should be able to analyze this content and extract useful information.
For example, it can find email addresses like test@example.com or contact@company.org.

It can also identify URLs like https://www.example.com or http://test.site/path?query=string.

The word frequency analysis will show that common words like 'the' and 'is' appear often,
while specific terms might appear less frequently.

For pattern matching, we can include special numbers like 123-45-6789 or dates like 2023-01-15.

Let's include another paragraph here to test paragraph counting.

And one more for good measure!"""
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(sample_text)
        print(f"Sample input file created at {file_path}")
    except Exception as e:
        print(f"Error creating sample file: {e}")

def main():
    # Initialize parser
    parser = TextFileParser()
    
    # Create sample input file
    input_file = "sample_input.txt"
    create_sample_input(input_file)
    
    # Analyze the file
    print(f"\nAnalyzing file: {input_file}")
    results = parser.analyze(input_file)
    
    if results:
        # Save results to file
        output_file = "analysis_report.txt"
        if parser.save_results(output_file):
            print(f"Analysis complete. Report saved to {output_file}")
            
            # Display some results in console
            print("\nSummary of findings:")
            print(f"- Word count: {results['statistics']['word_count']}")
            print(f"- Unique words: {results['word_frequency']['unique_words']}")
            print(f"- Emails found: {results['pattern_matches']['count']}")
            
            # Show the report content
            print("\nReport content:")
            with open(output_file, 'r', encoding='utf-8') as file:
                print(file.read())
        else:
            print("Failed to save analysis results.")
    else:
        print("File analysis failed.")

if __name__ == "__main__":
    main()