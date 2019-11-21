# itaipu  
  
Itaipu is a web app for managing a condominium, where residents can allow visitors, read notices and more!  
  
Following a very strict set of requirements, a django web app was developed for managing the client's condominium, carefully developed to respect the in-place infrastructure and to integrate with an existing MySQL database.    
    
Many solutions were created to overcome the challenges given by the great amount of requirements:    
    
1. A token system was designed for registering users and updating their record in the old database,    
2. Integration with an old system which needed to use the same database    
3. Developing a system resistant to local power/internet outages. Needed to be run locally, with little resources.    
4. Creating a hierarchy between users belonging to same property (owner, visitors, caretakers and residents)  

## Images:

### Desktop:

|                        Login: <img src="/docs/images/desktop/login.png" alt="Login" width="200"/>                       |         Create account: <img src="/docs/images/desktop/create_account.png" alt="Create account" width="200"/>        |           Home page: <img src="/docs/images/desktop/home_with_notice.png" alt="Home page" width="200"/>          |
|:----------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------:|
| Authorizing visit: <img src="/docs/images/desktop/authorize_visits2.png" alt="Authorize visits (editing)" width="200"/> | Editing property: <img src="/docs/images/desktop/property_config2.png" alt="Property config (editing)" width="200"/> |       Account config: <img src="/docs/images/desktop/account_config.png" alt="Account config" width="200"/>      |
|                  Notices: <img src="/docs/images/desktop/notices.png" alt="Notices page" width="200"/>                  |         Reading notice: <img src="/docs/images/desktop/notice_details.png" alt="Notice details" width="200"/>        | Notice marked as read: <img src="/docs/images/desktop/notice_read.png" alt="Notice marked as read" width="200"/> |

### Mobile:

|                        Login: <img src="/docs/images/mobile/login.png" alt="Login" width="200"/>                       |         Create account: <img src="/docs/images/mobile/create_account.png" alt="Create account" width="200"/>        |           Home page: <img src="/docs/images/mobile/home_with_notice.png" alt="Home page" width="200"/>          |
|:----------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------:|
| Authorizing visit: <img src="/docs/images/mobile/authorize_visits2.png" alt="Authorize visits (editing)" width="200"/> | Editing property: <img src="/docs/images/mobile/property_config2.png" alt="Property config (editing)" width="200"/> |       Account config: <img src="/docs/images/mobile/account_config.png" alt="Account config" width="200"/>      |
|                  Notices: <img src="/docs/images/mobile/notices.png" alt="Notices page" width="200"/>                  |         Reading notice: <img src="/docs/images/mobile/notice_details.png" alt="Notice details" width="200"/>        | Notice marked as read: <img src="/docs/images/mobile/notice_read.png" alt="Notice marked as read" width="200"/> |

### Account creation email:

![Create account - email](/docs/images/create_account_email.png)

Todo:
[rever status do git]