# Porter Stemmer

See implementation on 
[Jupyter Notebook](porter-stemmer-algorithm.ipynb).

The Porter stemming algorithm (or _Porter stemmer_) is a process for removing the 
commoner morphological and inflexional endings from words in English. Its main use is 
as part of a term normalisation process that is usually done when setting up 
Information Retrieval systems.

## Running Locally
Clone this repository from GitHun to your machine and navigate to the directory. Then run the 
driver file which will read the already present `resume.txt` file from directory and print the 
stemmed output. 
```bash
git clone https://github.com/anishLearnsToCode/porter-stemmer.git
cd porter-stemmer
python driver.py
```

If you wish to test some other file or some other english language string, simply naviagte to
the __driver.py__ file and modify the file path as
```python
from porter_stemmer import PorterStemmer
stemmer = PorterStemmer()
resume = open('your_file_path_here.xyz', 'r').read()
print(stemmer.stem_document(resume))
```

Or you can even stem custom strings as
```python
from porter_stemmer import PorterStemmer
stemmer = PorterStemmer()
print(stemmer.stem_sentence('The quick brown fox jumps over the lazy dog'))
``` 

## Usage
The `PorterStemmer()` class has the following 3 API end points
- `stem_word` Takes in a single word as _string_ and returns stemmed output also as _string_.
- `stem_sentence`: Takes in a single sentence as a _string_ e.g. `so many cats and dogs` and returns a
    stemmed _string_ like `so mani cat and dog`
- `stem_document`: This takes in an entiredocumentst as a _string_ and may have new line `\n` and `\t`
    tab space characters. e.g.
    ```text
    Do not go gentle into that good night,
    Old age should burn and rave at close of day;
    Rage, rage against the dying of the light.
    
    Though wise men at their end know dark is right,
    Because their words had forked no lightning they
    Do not go gentle into that good night.
    
    Good men, the last wave by, crying how bright
    Their frail deeds might have danced in a green bay,
    Rage, rage against the dying of the light.
    
    Wild men who caught and sang the sun in flight,
    And learn, too late, they grieved it on its way,
    Do not go gentle into that good night.
    
    Grave men, near death, who see with blinding sight
    Blind eyes could blaze like meteors and be gay,
    Rage, rage against the dying of the light.
    
    And you, my father, there on the sad height,
    Curse, bless, me now with your fierce tears, I pray.
    Do not go gentle into that good night.
    Rage, rage against the dying of the light
    ```
  
  The output will also be a _string_ like 
  ```text
   Do not go gentl into that good night
   Old ag should burn and rave at close of dai
   Rage rage against the dy of the light

   Though wise men at their end know dark i right
   Becaus their word had fork no lightn thei
   Do not go gentl into that good night

   Good men the last wave by cry how bright
   Their frail deed might have danc in a green bai
   Rage rage against the dy of the light

   Wild men who caught and sang the sun in flight
   And learn too late thei griev it on it wai
   Do not go gentl into that good night

   Grave men near death who see with blind sight
   Blind ey could blaze like meteor and be gai
   Rage rage against the dy of the light

   And you my father there on the sad height
   Curs bless me now with your fierc tear I prai
   Do not go gentl into that good night
   Rage rage against the dy of the light
  ``` 


## History
The original stemming algorithm paper was written in 1979 in the Computer Laboratory, Cambridge (England), as part of 
a larger IR project, and appeared as Chapter 6 of the final project report,

> C.J. van Rijsbergen, S.E. Robertson and M.F. Porter, 1980. New models in probabilistic information retrieval. 
>London: British Library. (British Library Research and Development Report, no. 5587).

With van Rijsbergen’s encouragement, it was also published in,
> M.F. Porter, 1980, An algorithm for suffix stripping, Program, 14(3) pp 130−137.

And since then it has been reprinted in
> Karen Sparck Jones and Peter Willet, 1997, Readings in Information Retrieval, San Francisco: Morgan Kaufmann, 
>ISBN 1-55860-454-4.

