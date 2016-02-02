from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast
import sys

# Read the whole text.
text = open(sys.argv[1]).read()
text = ast.literal_eval(text)
print text[1]

# Generate a word cloud image
wordcloud = WordCloud().generate_from_frequencies(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
