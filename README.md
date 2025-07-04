# Gift Pal - A Gift List Platform

Updated version by Geraldine Edwards (Originally created as a hackathon project named Gift Genie by: Phillip Kershaw, Christopher Matthew, Geraldine Edwards and Joanna O'Connor).

<img width="100%" alt="responsive screens landing page for the Gift Pal app" src="readme.docs/images/giftpal-lightmode.png">

<br>
<br>

> [View live project here](https://gift-Pal-91413d2174b0.herokuapp.com/)

Github links

> [View "Gift Pal" Github repo here](https://github.com/Gerbil1511/Gift-Pal)
>
> [View original hackathon project "Gift Genie" Github repo here](https://github.com/Philgck/gifting-genie-two)

Gift Pal is a dynamic and intuitive gifting management web application designed to help authenticated users manage their events and wishlist items, and connect with their friends to share and view profiles. Built with HTML, CSS, JavaScript, and Django, this app aims to streamline the process of organizing events, tracking desired gifts, and maintaining connections with friends, all in one place. Whether planning a birthday party, keeping track of gift ideas, or checking a friend's wishlist, Gift Pal makes the experience seamless and enjoyable. Gift Pal simplifies the process of managing gift lists and events while maintaining a social network of friends to share and celebrate with.

### Overview

<u>**Key Features:**</u>

**User Authentication:** Secure login and registration system to ensure user data privacy and personalized experience.

**Event Management:** Allows users to create, update, view, and delete events, complete with a calendar interface for date selection and event naming.

**Wishlist Management** Users can compile and manage a list of desired gifts, including item descriptions and purchase links.

**Friends List:** Users can add friends (other authenticated users), view their profiles, and see and like their events and wishlists, fostering a social aspect to gift-giving.

**CRUD Functionality:** Full Create, Read, Update, and Delete operations are supported across all models, providing flexibility and control to the users.

<u>**Models and Relationships:**</u>

**User:** Utilizes Django's built-in User model for handling authentication and user-related data.

**Event:** Links to the User model, allowing users to manage their events.

**WishlistItem:** Links to the User model, enabling users to manage their wishlist items.

**Friend:** Establishes a self-referential relationship within the User model, allowing users to connect and interact with friends.

<u>**Technical Stack:**</u>

**Front-End:** HTML, CSS, and JavaScript provide a responsive and user-friendly interface.

**Back-End:** Django handles the server-side logic, including database management and API development.

**Database:** Utilizes PostgreSQL to store and manage user data, events, wishlist items, and friendships.

**Deployment:** Configured for deployment on Heroku for accessibility and scalability.

---

## CONTENTS

- [User Experience](#user-experience)
  - Database planning
  - Purpose and intended audience
  - User stories
- [Creation process](#creation-process)
  - [Wireframes](#wireframes)
- [Design](#design)
  - Colour scheme
  - Typography
  - Imagery
- [Website features](#website-features)
- [Tablet/mobile view](#tablet/mobile-view)
- [Future features](#future-features)
- [Technologies used](#technologies-used)
- [Ai Augmentation](#ai-augmentation)
- [Deployment](#deployment)
- [Testing](#testing)
- [Credits](#credits)

---

 <br>

## USER EXPERIENCE

### Database Planning

---

NB: The User model is the standard Django Allauth model

**ERD of models Gift-Pal**

### User

| Field    | Type   | Notes       |
| -------- | ------ | ----------- |
| id       | int    | Primary Key |
| username | string |             |
| email    | string |             |
| ...      | ...    |             |

---

### WishlistCategory

| Field         | Type   | Notes              |
| ------------- | ------ | ------------------ |
| id            | int    | Primary Key        |
| name          | string |                    |
| slug          | string |                    |
| occasion_date | date   |                    |
| user_id       | int    | Foreign Key → User |
| ...           | ...    |                    |

**Relationship:**  
A `User` can have many `WishlistCategory` entries.

---

### WishlistItem

| Field       | Type   | Notes                          |
| ----------- | ------ | ------------------------------ |
| id          | int    | Primary Key                    |
| item_name   | string |                                |
| description | string |                                |
| link        | string |                                |
| priority    | string |                                |
| category_id | int    | Foreign Key → WishlistCategory |
| user_id     | int    | Foreign Key → User             |
| reserved_by | int    | Foreign Key → User (nullable)  |
| ...         | ...    |                                |

**Relationships:**

- A `WishlistCategory` can have many `WishlistItem` entries.
- A `User` can have many `WishlistItem` entries.
- A `WishlistItem` can be reserved by a `User`.

---

### Friendship

| Field     | Type   | Notes                     |
| --------- | ------ | ------------------------- |
| id        | int    | Primary Key               |
| user_id   | int    | Foreign Key → User        |
| friend_id | int    | Foreign Key → User        |
| status    | string | (e.g., pending, accepted) |
| ...       | ...    |                           |

**Relationship:**  
A `User` can have many `Friendship` entries (as user or friend).

---

### Event

| Field   | Type     | Notes              |
| ------- | -------- | ------------------ |
| id      | int      | Primary Key        |
| title   | string   |                    |
| start   | datetime |                    |
| end     | datetime |                    |
| user_id | int      | Foreign Key → User |
| ...     | ...      |                    |

**Relationship:**  
A `User` can have many `Event` entries.

---

Relationships Summary

- **User** 1---\* **WishlistCategory**
- **WishlistCategory** 1---\* **WishlistItem**
- **User** 1---\* **WishlistItem**
- **WishlistItem** \*---1 **User** (reserved_by)
- **User** _---_ **Friendship** (_as user or friend_)
- **User** 1---\* **Event**
  <br>
  <br>

**Purpose and Intended Audience of Gift-Pal**

PURPOSE

Gift-Pal is designed to simplify and enhance the experience of managing events, gift wishlists, and social connections. Its primary goal is to provide users with an efficient, user-friendly platform to keep track of important dates, desired gifts, and their network of friends. By integrating event management, wishlist tracking, and friend interactions in a single application, Gift-Pal aims to make gift-giving and event planning more organized and enjoyable.

INTENDED AUDIENCE

- Gift-Pal caters to a diverse audience, including:
- Individuals: Anyone looking to manage their personal events, keep a list of gift ideas, and connect with friends to share and view wishlists and event details.
- Families and Friends: Groups of users who want to coordinate gift-giving and event planning within their social circles, ensuring everyone is on the same page for special occasions.
- Event Planners: Professionals or enthusiasts who need a reliable tool to organize events, track important dates, and manage guest lists and gift registries.
- Communities and Clubs: Social groups and organizations that want to maintain a shared calendar of events and coordinate gift exchanges among members.

By addressing the needs of these varied user groups, Gift-Pal aims to create a cohesive and interactive experience that brings people together through thoughtful event planning and gift-giving.

**Gift-Pal User stories**

| Title                     | User story                                                                                                                    | MoSCoW prioritisation |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **Account Registration**  | As a **site user** I want to **register an account** so that I can **login and access my personalized dashboard.**            | Must have             |
| **User Login**            | As a **registered user** I want to **log in to my account =** so that I can **access my events, wishlist, and friends list.** | Must have             |
| **Event Creation**        | As a **registered user** I want to **create events** so that I can **manage my schedule and important dates.**                | Must have             |
| **Add Wishlist Item**     | As a **registered user** I want to **add items to my wishlist** so that I can **keep track of gifts I want to receive.**      | Must have             |
| **Edit Profile**          | As a **registered user** I want to **edit my profile** so that I can **update my personal information.**                      | Must have             |
| **Delete Event**          | As a **registered user** I want to **delete an event** so that I can **remove it from my calendar.**                          | Must have             |
| **Add Friends**           | As a **registered user** I want to **add friend** so that I can **view their events and wishlist, and they can view mine.**   | Should have           |
| **View Friend's Profile** | As a **registered user** I want to **view my friend's profile** so that I can **see their events and wishlist.**              | Should have           |
| **View Friend's Profile** | As a **registered user** I want to **view my friend's profile** so that I can **see their events and wishlist.**              | Could have            |

<p align="right"><a href="#contents">Back To Table of Contents</a></p>

---

### CREATION PROCESS

[GitHub Projects](https://github.com/users/Philgck/projects/13) was used to create a project board and was populated with user stories and added labels according to MoSCoW prioritisation.
All but one of the 'must have' user stories were completed with any other issues being carried over to the next sprint of the project development.

![Project Board](readme.docs/images/project_board.png)

Each user story had acceptance criteria added.The fulfillment of the criteria for each of these can be demonstrated by the presence of the features on the site (see below). The CRUD funtionality of the 'Event', 'Wish List' and 'Friends' models were tested extensively throughout each development phase both manually and through automated unit tests.

---

**Gift-Pal SITE USER GOALS**

- Efficient Event Management:
- Users want to easily create, update, and delete events for important occasions.
- Users aim to view a comprehensive list of their upcoming events and associated details.
- Streamlined Gift Management:
  - Users want to add, update, and delete items in their wishlist.
  - Users aim to view and manage a consolidated list of desired gifts with links for easy access.
- Social Connectivity:
  - Users want to add friends and view their profiles.
  - Users aim to see their friends' events and wishlists to stay informed.
- Personalized User Experience:
  - Users want to edit their profile information to keep it up-to-date.
  - Users aim to receive personalized notifications and updates about their events and friends' activities.
- Privacy and Security:
  - Users want to ensure their personal data is secure.
  - Users aim to manage their privacy settings for who can view their profile and content.

**Gift-Pal SITE-OWNER GOALS**

- User Engagement:
  - Site owners want to increase user registration and activity on the platform.
  - Site owners aim to keep users engaged with regular updates and new features.
- Platform Maintenance:
  - Site owners want to ensure the application runs smoothly without downtime.
  - Site owners aim to regularly update the app with bug fixes and performance improvements.
- Data Analytics:
  - Site owners want to collect and analyze user data to improve the app's features.
  - Site owners aim to use analytics to understand user behavior and preferences.
- Security Compliance:
  - Site owners want to comply with data protection regulations.
  - Site owners aim to implement robust security measures to protect user data.
- Community Building:
  - Site owners want to foster a strong community of users.
  - Site owners aim to create engagement opportunities such as forums, newsletters, and social media integration. (FUTURE FEATURE)

<p align="right"><a href="#contents">Back To Table of Contents</a></p>

---

## CREATION PROCESS

### Wireframes

There was a moderate redesign of the UI of the original project Gift-Genie, however some similarities remain.

<details open>
<summary>Landing page wireframe desktop view </summary>
<img width="1080" alt="Landing page wireframe" src="readme.docs/images/wireframe_landing page.png">
</details>

<details>
<summary>Landing page view for tablet and mobile devices</summary>
<img width="1080" alt="Landing Page responsive wireframes" src="readme.docs/images/wireframes_landing_page_responsive.png">
</details>

<details>
<summary>Registration page view wireframe</summary>
<img width="1080" alt="Registration page wireframe" src="readme.docs/images/wireframe_login_registration.png">
</details>

---

## DESIGN

### Typography

The website uses the following fonts:

- **Ubuntu**: The primary font used throughout the website for its clean and professional appearance. Ubuntu is a widely available sans-serif font that ensures readability and consistency across different devices and browsers.

### Colour Scheme

The color scheme of the website is was taken from open source Bootswatch (https://bootswatch.com/quartz/) and we chose the Quartz theme which provides a fun and colourful background and a non-intrusive background that is easily viewed in both light and dark modes. This design was chosen as it had a fun and warm feel to associate with gift-giving occasions.

### Imagery

- **Pixabay**: Royalty-free stock images that are used to complement the content. [Pixabay](https://pixabay.com/)

The 'Gift Pal' icon is used as the icon to enhance the visual appeal and usability of the website. The same icon is included both on each page in the Navbar and as a recognisable icon as the favicon for the tab. [Procreate](https://procreate.com/)
![favicon and icon](readme.docs/images/icon_and_favicon.png)

### Layout and Styling

The website features a consistent layout and styling across all pages, ensuring a cohesive user experience. Key design elements include:

- **Header**: The header contains a collapsible navbar that is consistent across all pages. It includes links to the main sections of the website, profile, planner, friendslist and user wishlists. The navbar also includes login and signup links for unauthenticated users and a logout button for authenticated users.
- **Collapsible Navbar**: The navbar is designed to be responsive and collapses into a hamburger menu on smaller screens. This ensures that the navigation is accessible and user-friendly on all devices.
- **Footer**: The footer is consistent across all pages and includes links to social media apps Facebook, X (formerly Twitter), Instagram and LinkedIn. It also includes links to the terms & conditions, privacy policy and site map pages. The styling is cohesive across all pages to give a cohesive look and feel across all pages.
  ***
  <p align="right"><a href="#contents">Back To Table of Contents</a></p>

## WEBSITE FEATURES

**LANDING PAGE VIEW**

  <details open>
  <summary>landing page</summary>

![home-page](readme.docs/images/landing1.png)
![home-page cont.](readme.docs/images/landing2.png)
![home-page cont.](readme.docs/images/landing3.png)
![home-page cont.](readme.docs/images/landing4.png)

  </details>
  Users arrive directly on the landing page which outlines the purpose of the app immediately rather than requiring users to log in or register before being able to see anything in order to entice users to then sign-up in order to use the features.

<br>

**USER AUTHENTICATION**

<details open>
  <summary>Authentication page</summary>

![Signup Page](readme.docs/images/signup_page_view.png)
![login-page](readme.docs/images/login_page_view.png)
![sign-out-page](readme.docs/images/sign_out_confirm.png)

Users must be registered via the sign up page and/or login to navigate from the landing page to their user profile. Incomplete fields will receive prompts. A signout confirmation is requested if a user selects to sign out.

**USER PROFILE VIEW**

  <details open>
  <summary>User Profile Page</summary>

![User Profile Page](readme.docs/images/user_profile_page_view.png)
![User Profile Page Cont.](readme.docs/images/user_profile_page_view2.png)

  </details>
  Authenticated users then access their calendar to add, view or edit events; access wishlists to add, view or modify categories and items, and access their friends list to view or modify their friends list from the navbar at all times. 
  
<br>
    
  **EVENTS DETAILED VIEW**
  <details>
  <summary>Calendar of events</summary>

![events-detail](readme.docs/images/populated_planner_view.png)

  </details>
  The detailed view a calendar containing user added events.

  <br>

**WISHLIST VIEW**

  <details>
  <summary>A populated wishlist example</summary>

![comment](readme.docs/images/my_wishlist_populated_view.png)

  </details>
  Each user can add/manage categories for wishlists and add/manage wishlist items in each category.

<br>

**FRIENDS LIST VIEW**

  <details>
  <summary>Example associated Friends List</summary>

![comment](readme.docs/images/basic_friends_list_for_user_1.png)

  </details>
  Each user can search and make a request to befriend other registered users or manage their existing friends list 
  
<br>

## FUTURE FEATURES

The following would be options to consider including in future versions of the website:

- Include a 'Share Wishlist' or 'Share Events' feature so authenticated users can share new or edited items/events with with their family and friends

- Requested friends can receive notifications (via a preferred method eg email or in-app) when other users edit their wishlist to indicate intention of purchase.

- Friends can receive notifications (via a preferred method eg email or in-app) that another friend has created a new event or wishlist.

---

<p align="right"><a href="#contents">Back To Table of Contents</a></p>

## TECHNOLOGIES USED

### Languages Used

![Python](https://img.shields.io/badge/Python-3.8-blue)
![asgiref](https://img.shields.io/badge/asgiref-3.8.1-blue)
![cloudinary](https://img.shields.io/badge/cloudinary-1.41.0-blue)
![dj-database-url](https://img.shields.io/badge/dj--database--url-0.5.0-blue)
![gunicorn](https://img.shields.io/badge/gunicorn-20.1.0-blue)
![oauthlib](https://img.shields.io/badge/oauthlib-3.2.2-blue)
![psycopg](https://img.shields.io/badge/psycopg-3.2.1-blue)
![PyJWT](https://img.shields.io/badge/PyJWT-2.9.0-blue)
![python3-openid](https://img.shields.io/badge/python3--openid-3.2.0-blue)
![requests-oauthlib](https://img.shields.io/badge/requests--oauthlib-2.0.0-blue)
![sqlparse](https://img.shields.io/badge/sqlparse-0.5.1-blue)
![urllib3](https://img.shields.io/badge/urllib3-1.26.19-blue)
![whitenoise](https://img.shields.io/badge/whitenoise-5.3-blue)

### Frameworks, Libraries, and Programs Used

![Bootstrap](https://img.shields.io/badge/Bootstrap-4.6-blue)
![Balsamiq](https://img.shields.io/badge/Balsamiq-Wireframes-orange)
![Git](https://img.shields.io/badge/Git-2.32.0-brightgreen)
![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)
![Django](https://img.shields.io/badge/Django-Framework-green)
![Contrast Finder](https://img.shields.io/badge/Contrast%20Finder-Tool-yellow)
![TinyPNG](https://img.shields.io/badge/TinyPNG-Image%20Compression-green)
![Chrome Dev Tools](https://img.shields.io/badge/Chrome%20Dev%20Tools-Tool-blue)
![Lighthouse](https://img.shields.io/badge/Lighthouse-Performance-orange)
![Favicon.io](https://img.shields.io/badge/Favicon.io-Tool-yellow)
![W3Schools](https://img.shields.io/badge/W3Schools-Resource-green)
![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Resource-orange)
![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-AI%20Assistant-blue)
![Perplexity](https://img.shields.io/badge/Perplexity-Tool-lightgrey)
![Wikipedia](https://img.shields.io/badge/Wikipedia-Resource-blue)
![Font Awesome](https://img.shields.io/badge/Font%20Awesome-Icons-blue)
![W3C HTML Validator](https://img.shields.io/badge/W3C%20HTML%20Validator-Pass-brightgreen)
![W3C CSS Validator](https://img.shields.io/badge/W3C%20CSS%20Validator-Pass-brightgreen)
![JSHint](https://img.shields.io/badge/JSHint-JavaScript%20Validator-yellow)
![PEP8](https://img.shields.io/badge/PEP8-Python%20Style%20Guide-blue)
![Adobe Color](https://img.shields.io/badge/Adobe%20Color-Tool-orange)
![CI Python Linter](https://img.shields.io/badge/CI%20Python%20Linter-Pass-brightgreen)
![Microsoft Copilot](https://img.shields.io/badge/Microsoft%20Copilot-AI%20Assistant-blue)
![DeepSeek](https://img.shields.io/badge/DeepSeek-AI%20Assistant-green)
![Perplexity AI](https://img.shields.io/badge/Perplexity%20AI-AI%20Assistant-lightgrey)
![Summernote](https://img.shields.io/badge/Summernote-WYSIWYG%20Editor-blue)
![Heroku](https://img.shields.io/badge/Heroku-Hosting-purple)
![Diffchecker](https://img.shields.io/badge/Diffchecker-Tool-blue)
![Flexbox](https://img.shields.io/badge/Flexbox-CSS%20Layout-blue)
![Pixabay](https://img.shields.io/badge/Pixabay-Image%20Library-green)

---

 <p align="right"><a href="#contents">Back To Table of Contents</a></p>

### AI AUGMENTATION

### Leveraging AI Tools for Code Creation

During the development of the Gift Pal app, GitHub Copilot, Chat GPT and DeepSeek was utilized to assist in code creation. Each AI solution provided valuable code snippets and suggestions that accelerated the development process. Key areas where AI was used include:

- **Generating Views and Templates**: AI was instrumental in generating Django views and HTML templates. These snippets provided a solid foundation, which were then manually checked and modified to fit the project's specific requirements.
- **Form Handling**: AI assisted in creating forms for user input. The generated code snippets were reviewed and adjusted to ensure they met the application's validation and processing needs.
- **File and Directory Management**: AI was invaluable in the reminding of the numerous files and directories to amend when new models, views, or features were introduced, ensuring that all the correct files were updated.
  While AI provided a significant boost in productivity, it was essential to manually review and modify the generated code to ensure accuracy and alignment with project requirements.

### AI-Assisted Debugging

GitHub Copilot and DeepSeek played a crucial role in identifying and resolving bugs. Key interventions include:

- **Error Handling**: AI suggested error handling mechanisms for example, it provided initial code for handling form validation errors, which were then refined to improve user feedback and error reporting.
- **Debugging Views**: When encountering issues with view logic, AI suggested potential fixes and improvements. These suggestions were cross-referenced with the current code using tools like Diffchecker and W3C to ensure the changes were appropriate and did not introduce new issues.
  Manual use of Diffchecker was crucial in comparing AI's suggestions with the existing codebase, ensuring that only the most relevant and accurate changes were implemented.

### Optimizing Code for Performance and User Experience

AI was also used to optimize code for performance and enhance user experience:

- **Efficient Query Handling**: AI suggested optimizations for database queries to reduce the number of database hits and improve performance.
- **Responsive Design**: AI provided initial CSS and JavaScript snippets to enhance the application's responsiveness. These snippets were manually adjusted to ensure a seamless user experience across different devices using custom color choices and fonts, as well as Bootstrap and Flexbox for structure and positioning.

### Generating Django Unit Tests

AI assisted in generating Django unit tests to ensure code coverage for key functionalities:

- **Test Logic Generation**: GitHub Copilot generated initial test cases for views, forms, and models. For example, it provided test cases for creating, editing, and deleting wishlist items, as well as adding and removing friends. These tests were reviewed and adjusted to improve accuracy and completeness.
- **Ensuring Code Coverage**: GitHub Copilot's suggestions helped ensure all critical paths were tested. For instance, it generated tests for edge cases, such as handling invalid form submissions and testing user permissions. The generated test logic demonstrated a basic understanding of the application's functionality, and manual adjustments were made to ensure the tests accurately reflected the intended behavior.

### Additional AI Tools

In addition to GitHub Copilot, Chat GPT and DeepSeek, other AI tools were leveraged in much lesser forms:

- **Perplexity**: Used for generic questions regarding feature planning and implementation, providing valuable insights and information.
- **Microsoft Copilot**: Assisted in generating user stories and blog content based on key information provided by the developer

### Reflection on AI Tools

Using GitHub Copilot, DeepSeek, Chat GPT and other AI tools significantly enhanced the development process by providing relevant code snippets and suggestions. They accelerated the initial coding phase, assisted in debugging, and ensured comprehensive test coverage. However, it was essential to manually review and adjust the generated code to ensure it met the project's specific requirements and maintained high standards of quality and performance. AI can occasionally repeat itself despite clear prompts, as if it 'forgets' the previous steps or the focus of the initial query, which can be time-consuming. It is crucial to know when to manually take over reviewing the code.

---

<p align="right"><a href="#contents">Back To Table of Contents</a></p>

## DEPLOYMENT of Gift-Pal

The site was deployed to Heroku. The steps to deploy are as follows:

- Install the gunicorn python package and create a file called 'Procfile' in the repo's root directory
- In the Procfile write 'web: gunicorn nuclear_knowledge.wsgi:application --log-file -'
- In settings.py add ".herokuapp.com" to the ALLOWED_HOSTS list
- In settings.py add 'https://\*.herokuapp.com' to CSRF_TRUSTED_ORIGINS list, git add, commit and push to github

Navigate to the Heroku dashboard

- Create a new Heroku app
- Give it a name and select the region 'Europe'
  Navigate to settings tab and scroll down to Config Vars
- Click 'Reveal Config Vars'
- Add the following keys:
  key = DATABASE_URL | value = (my secret database url)
  key = SECRET_KEY | value = (my secret key)
  Navigate to Deploy tab
- Connect to GitHub and select the repo 'gift-pal'
- Scroll down to 'Manual deploy' and select the 'main' branch
- Click 'Deploy Branch'

---

<p align="right"><a href="#contents">Back To Table of Contents</a></p>

## TESTING

The W3C Markup validator was used to validate all HTML code - [W3C Markup Validator](https://validator.w3.org/)

Throughout this project DTL was utilised. The HTML validator often throws errors when using DTL therefore the following approach was used:

- navigate to the deployed Heroku link
- right click to find the 'view page source' link
- copy and paste the HTML code from here into the validator via the direct input

[home page html validation](readme.docs/...)

[A MODEL page html validation](readme.docs/...)

### CSS validation

[CSS validation](readme.docs/...)

[W3C CSS Validator](https://jigsaw.w3.org/css-validator/) was used to validate the CSS file. External CSS for Bootstrap, provided by [CDN](https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/css/bootstrap.min.css) was not tested.

### Javascript validation

[JavaScript Validator](https://jshint.com) - the JavaScript validator was to be used - did not throw up and issues.

### Python validation

[CI Python Linter](https://pep8ci.herokuapp.com/#) will be used to validate the python code.

### Lighthouse scores from Heroku deployed app via Chrome dev tools

![lighthouse](readme.docs/images/lighthouse_desktop.png)
![lighthouse](readme.docs/images/lighthouse_mobile.png)

The recent Lighthouse audit yielded excellent performance scores for the desktop version of our application. This achievement reflects the hard work and dedication of the development team in optimizing the user experience for desktop users. However, it was also noted that the mobile performance scores were not up to expectations. Recognizing the importance of a seamless mobile experience, addressing these issues in the upcoming sprint is a huge priority. The team is committed to enhancing mobile performance to ensure that all users, regardless of their device, enjoy a fast and responsive application.

### Manual Testing

## Manual Testing Checklist

| Feature                | Test Case                                                                | Pass/Fail | Notes |
| ---------------------- | ------------------------------------------------------------------------ | --------- | ----- |
| **Authentication**     | Login with valid credentials                                             |           |       |
|                        | Logout and confirm redirect to login/landing page                        |           |       |
|                        | Access protected page after logout (should redirect to login)            |           |       |
| **Profile Management** | View profile details after login                                         |           |       |
|                        | Edit profile details and confirm changes                                 |           |       |
|                        | Change profile picture and confirm update                                |           |       |
|                        | Remove profile picture and confirm default appears                       |           |       |
| **Wishlist**           | Add wishlist category and confirm it appears                             |           |       |
|                        | Add wishlist item to category and confirm it appears                     |           |       |
|                        | Edit wishlist item and confirm changes                                   |           |       |
|                        | Delete wishlist item and confirm removal                                 |           |       |
|                        | Delete wishlist category and confirm all items are removed               |           |       |
| **Friends**            | Add friend (send and accept request) and confirm in friends list         |           |       |
|                        | Remove friend and confirm removal from both users' lists                 |           |       |
|                        | Check pending friend requests for both sender and receiver               |           |       |
| **Events**             | Add event and confirm it appears in calendar/list                        |           |       |
|                        | Edit event and confirm changes                                           |           |       |
|                        | Delete event and confirm removal                                         |           |       |
| **Navigation**         | Navigate between all main pages using navbar                             |           |       |
|                        | Check footer links (Terms, Privacy, Site Map, Social) open correct pages |           |       |
| **Validation**         | Try submitting forms with invalid/empty input and check error handling   |           |       |

<br>

### Agile Process for Gift-Pal

An agile methodology was adpted using a GitHub project board, applying MoSCoW prioritization to manage my tasks. The board was regularly updated to ensure all 'Must have' and 'Should have' features were addressed. Some 'Could have' issues remain in the backlog for future sprints, as detailed in the 'Future Features' section below.

---

<p align="right"><a href="#contents">Back To Table of Contents</a></p>

## CREDITS

**Content**

- [JoannaOConnor/readme-example on GitHub](https://github.com/JOCPhys/Nuclear-Knowledge-JOC/blob/main/README.md)
  was used to help write the README.md
- [Code Institute Sample README](https://github.com/Code-Institute-Solutions/SampleREADME)
  was used as a reference when writing the README.
- [Code Institute](https://learn.codeinstitute.net/) The IDE was used for extra reference for HTML, CSS, Python and Django

**Media**

- All images not generated from DALL.E AI were obatined from:
- [Amiresponsive](https://ui.dev/amiresponsive) for the responsivity mockup on the README.
- [Ignore X frame headers](https://chromewebstore.google.com/detail/ignore-x-frame-headers/gleekbfjekiniecknbkamfmkohkpodhe)
  was used to download a Chrome extension to allow the resposivity image to be taken.
- [CODE OPEN IO](https://codepen.io/RoyLee0702/pen/RwNgVya) was used to create the giftbox animation
- [BOOTSWATCH](https://bootswatch.com) was used for the css styling using the Quartz theme

**Acknowledgements**

- Code Institute Facilitator Dillon McCaffrey for his encouragement, patience, guidance and support.
- Code Institute SME Coach John Rearden for coding advice
- Code Institue Coding Coach Ruairidh MacArthur for GIT advice

<p align="right"><a href="#contents">Back To Table of Contents</a></p>
