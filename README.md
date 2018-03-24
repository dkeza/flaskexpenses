I am creating this web app to learn Python and Flask Webframework.

It should be possible that users can log in, and create accounts.
For every account should be possible to enter incomes and expenses.

## First install

I am using Windows OS.
Python 3.6 is needed.
Start command prompt.
Create new directory, and CD into it.

Rename run.example.bat to run.bat, and edit and set enviroment variabels.
Call vinit.bat, to set Python environment and download needed modules.

Install all Python modules:

```
python -m pip install -r requirements.txt
```

You must also initialize database with this command:

```
flask db upgrade
```

Now call run.bat

To start this app later, start command prompt, CD into app directory, call vactivate.bat, and then run.bat

## Internationalization

To add new language:

```
flask translate init <language-code>
```

To update translations

```
flask translate update
```

To compile all languages

```
flask translate compile
```