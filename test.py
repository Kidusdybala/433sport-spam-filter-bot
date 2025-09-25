import re

# List of abusive words (add more as needed)
ABUSIVE_WORDS = [
    'fuck', 'shit', 'damn', 'bitch', 'asshole', 'bastard', 'cunt', 'dick', 'pussy',
    'nigger', 'faggot', 'retard', 'whore', 'slut', 'crap', 'bullshit', 'suck',
    'dumbass', 'idiot', 'stupid', 'moron', 'jerk', 'prick', 'twat', 'wanker',
    'ጭቅቅታሙ', 'ውሻ', 'ጥንቡ', 'አህያ', 'ተበዳ', 'ሲበዳ', 'አይጥ', '💩', '🐀', '🐪', '🐫', 'ቂጥ', 'ፔሬድ', 'የወር አበባ',
    'ቁላ', 'ተኮላሸ', 'ፈርሴ', 'Netflix', 'ሽባ', 'ቀነዘረ', 'ጭገራም', 'tebeda', 'fara', 'ahya', 'qeshim', 'ems', 'gim', 'tenb', 'tnb', 'ላም', 'ላሟ', 'lam', 'lemagn', 'ለማኝ', 'ዲቻ', 'ቆቦ',
    'ወሸላ', 'የለማኝ ልጅ', 'yelemagn lej', 'ሸርሙጣ', 'ቡሽጢ', 'ቡሽቲ', 'bushti', 'jezba', 'ጀዝባ', 'እከካም', 'እከክ', 'ekekam', 'ekek', 'tija', 'ጥጃ', 'ዝንጀሮ', 'zenjero',
    'ቡሌ', 'ሌስትሮ', 'ሊስትሮ', 'ቆሎ', 'ሸታታ', 'የሚሸት', 'ፋንድያ', 'qolo', 'shetata', 'yemishet', 'listro', 'entenh', 'እንትንህ', 'አይምሮህ', '🧠', 'denez', 'dengay', 'ደነዝ', 'ድንጋይ', 'tnbu', 'sedb', 'ስድብ', 'temar', 'ተማር', 'temr', 'ፓንት', 'አዟሪ', 'pant', 'azuari', 'beg', 'በግ', 'ግመል', 'camel', 'gemel', 'መሃይቡ', 'መሀይሙ', 'mehaymu', 'terfrafi', 'ትርፍራፊ', 'ከብት', 'kebt', 'ሽማግሌ', 'በክት', 'bekt', 'jel', 'ጅል', 'ላጭቼ', 'ላጭ', 'ቂንጥር', 'ቆለጥ', 'እንዳልቨዳ', 'ጭቅቅታም',
    'ሸሌ', 'ጭገር', 'ጥንብ', 'ሸተቱ', 'ቆሻሻ', 'እበት', 'ሹጢ', 'ደደብ', 'ተበጂ', 'ጡት', 'ኩበት', 'ጡቷ'
]

def generate_fuzzy_pattern(word):
    """Generate a regex pattern that matches the word with repeated characters."""
    return ''.join(f'{re.escape(c)}+?' for c in word)

ABUSIVE_PATTERNS = [generate_fuzzy_pattern(word) for word in ABUSIVE_WORDS]

# The message to test
message = "hey guys its not about muslim or christianity gn esraeln mtdegfu sewoch hilina yinurachu gaza ley emimotew eko dmet adelem sew enji christianity eko gdel aylm degmo esrael eko eske ahun chraistosn matak hager nech"
text = message.lower()

# Check which patterns match
matching_indices = []
for i, (word, pattern) in enumerate(zip(ABUSIVE_WORDS, ABUSIVE_PATTERNS)):
    if re.search(pattern, text, re.IGNORECASE):
        matching_indices.append(i)

print("Matching abusive word indices:")
for idx in matching_indices:
    print(idx)
print("Matching words:")
for idx in matching_indices:
    print(ABUSIVE_WORDS[idx])
print("Total matches:", len(matching_indices))