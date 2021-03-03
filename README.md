# staticconfig

Json config files with a staticly defined structure.

This is common code which I used accross many projects.

## Usage

A config file's structure is defined by subclassing `Config` and filling the constructor with attribute assignments.

Then a file is loaded with the `from_json` classmethod:

- If the file exists, it returns an instance of the config class.
- If the file does not exist, it creates one and raises a ConfigError.

The class `Namespace` provides syntactic sugar around dicts.

### Example

```python
from staticconfig import Namespace, Config


class MyConfig(Config):

  def __init__(self):
    super().__init__()
    
    self.option1 = "default1"
    self.option2 = 0
    self.option3 = Namespace()
    self.option3.suboption1 = True
    self.option3.suboption2 = ["en", "de"]
    

# If the file doesn't exists this will create it with the default values and raise a ConfigError
config = MyConfig.from_json("config.json")
```

The produced config file:
```json
{
  "option1": "default1",
  "option2": 0,
  "option3": {
    "suboption1": true,
    "suboption2": [
      "en",
      "de"
    ]
  }
}
```
