*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  validuser
    Set Password  valid123
    Set Password Confirmation  valid123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ab
    Set Password  valid123
    Set Password Confirmation  valid123
    Click Button  Register
    Register Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  validuser
    Set Password  short1
    Set Password Confirmation  short1
    Click Button  Register
    Register Should Fail With Message  Password must be at least 8 characters long

Register With Valid Username And Invalid Password
    Set Username  validuser
    Set Password  onlyletters
    Set Password Confirmation  onlyletters
    Click Button  Register
    Register Should Fail With Message  Password must contain non-letter characters

Register With Nonmatching Password And Password Confirmation
    Set Username  validuser
    Set Password  valid123
    Set Password Confirmation  different123
    Click Button  Register
    Register Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  valid123
    Set Password Confirmation  valid123
    Click Button  Register
    Register Should Fail With Message  Username is already in use

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
