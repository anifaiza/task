# Library Management System
This is the design of the backend of a 'Library Website'. The design pattern goes as follows.
## Object Model
* User :
    * id
    * name
    * username
    * email
    * password
    * role
* Book :
    * id
    * name
    * author
    * publisher
    * publishing date

## Model URI
>http://localhost/user Method: GET

>http://localhost/user Method: POST

>http://localhost/book Method: POST

>http://localhost/book Method: GET

>http://localhost/book/:id Method: GET

>http://localhost/book/:id Method: PUT

>http://localhost/book/:id Method: DELETE

## Data representation
### Single data representation

>Book

    {
        id: 1
        name: 'book1'
        author: 'author_1'
        publisher: 'publisher_1'
        publish_date: 'Jan 2000'
    }

### Multiple data representation

>Book

    [
        {
            id: 1
            name: 'book1'
            author: 'author_1'
            publisher: 'publisher_1'
            publish_date: 'Jan 2000'
        },
        {
            id: 2
            name: 'book2'
            author: 'author_2'
            publisher: 'publisher_2'
            publish_date: 'Jan 2000'
        }
    ]

## JSON View

>Book

Single data 

    [
        {
            "id" : "1",
            "name" : "book1",
            "author" : "author_1",
            "publisher" : "publisher_1",
            "publish_date" : "Jan 2000"
        }
    ]

Multiple data

    [
        {
            "id" : "1",
            "name" : "book1",
            "author" : "author_1",
            "publisher" : "publisher_1",
            "publish_date" : "Jan 2000"
        },
        {
            "id" : "2",
            "name" : "book2",
            "author" : "author_2",
            "publisher" : "publisher_2",
            "publish_date" : "Jan 2000"
        }
    ]
