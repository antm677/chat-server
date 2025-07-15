```markdown
## Promo codes

✨ Introduce a new bonus type "Purchase Discount"

Users will be allowed to enter a promo code when purchasing a package. When entered, it should give a discount on the package price.

Currently supported types:

*   Instant transaction
*   Insured position
*   Spread Discount
*   Vault
*   Signals

Add **Purchase Discount** to the above types.

```
  
  Purchase discount
  Discount (%)
  50%
```

Purchase discount can not be combined with any other bonus type. Therefore, the **Purchase discount** checkbox should be disabled if any other bonus type is selected and vice versa, when **Purchase discount** is selected, other bonus types should be disabled.
``````markdown
# Margin coefficient

✨ Initial margin and maintenance calculations for Quantum accounts.

Challenge definitions have **Margin coefficient** parameter which should be applied when calculating margin to open a position and when margin to maintain a position.

Example:

Assuming that **Initial margin** for EURUSD is set to 0.1:

*   If Margin coefficient = 1:
    *   the resulting initial margin for EURUSD when user opens a position would be `0.1 * 1 = 0.1`
*   If Margin coefficient = 0.5:
    *   the resulting initial margin when user opens a position would be `0.1 * 0.5 = 0.05`
*   If Margin coefficient = 1.5:
    *   the resulting initial margin when user opens a position would be `0.1 * 1.5 = 0.15`

Similar logic applies to maintenance margin coefficient, i.e. `maintenance_margin * margin_coefficient`.
``````markdown
## Challenge and Package updates

1.  Add **Challenge name** text field and **Allow profit sharing** checkbox to Challenge view and challenge form and portfolio.  [Back Office - Dealing](https://www.google.com)

2.  Add **Available from, Available until, Daily loss, Max loss, and Learn more** fields to the Package view and package form.

3.  Make the Package form a full screen form (like trading groups for example:  [Back Office - Dealing](https://www.google.com) )

    ```
    Add new Package

    Package name *   | Brand *       | Visible
    Apply for $10,000| A3Trading     |
    Package description *              | Label *
    Evaluation Funding Capital $5,000 | A3Trading_ES
    Learn more *
    https://www.tradeapp.com/faq

    Leverage * | Initial balance * | Full price * | Discounted price *
    1:30       | 0.00            | 100.00      | 100.00
    Daily loss (%) * | Max loss (%) *   | Available from *  | Available until *
    5          | 8               | 01.08.2025  | 01.09.2025
    Minimum trading days |
    0                | Add-ons:       |
                      | - Higher profit share
                      | - Double leverage
                      | - Hybrid max loss / profit target
                      | - No minimum trading days
    Next challenge: |    |  Clear selection

    Id  | Group
    ----|-----
    123 | Quantum challenge 2
    123 | Quantum challenge 3

    ```

4.  Add the **Challenge** filter to Portfolio | Dealing | Closed positions.

    ```
    Closed Positions (0)  Jul 8, 2025 - Jul 9, 2025
    Symbol | Position ID | Direction | Open Date | Open Rate | Close Date
    ```

5.  Add the **Challenge** filter to Portfolio | CRM | Retention tools | Challenge

---

**Challenge Information**

```
Call  ✔  Feedback Email ME SMS
Schedule
Online Chat
Interactions Activities Registration Attempts Retention Tools Correspondence Change Log

Challenge             | Challenge
Evaluation phase      |  Evaluation phase

Profit target:  10%     | Loss alert level:  0%
Trader Profit Share: 80%  | Minimum trading days: 5
Reward Type: Payout      | Withdrawals delay: 5 days
Daily loss 5%          | Margin coefficient: 1
Max Loss 8%            | Weekend trading
```

Challenge state:  Failed
```
```markdown
# Sign-up and Purchasing packages

Process flow chart:

```mermaid
graph TD
    A[Sign up from tradeapp.com] --> B{Create Quantum account in the default trading group, disable quantum session}
    B --> C[Purchase Package]
    C --> D{Add initial credits, activate Quantum session, set expiry date}
    D --> E{Create Challenge history record using challenge and add-on settings}
    style E fill:#f9f,stroke:#333,stroke-width:2px
    classDef new fill:#009900,stroke:#333,stroke-width:2px
    classDef active fill:#999999,stroke:#333,stroke-width:2px
    class E new
    class E "Challenge status: New"

```

*   Sign-up flow starts from tradeapp.com. Upon signing up, a new lead should be created without an account. Users should land on the packages page and in the platform.
*   When user purchases a new Package, the payment needs to be registered as Deposit transaction (similar to Academy package purchase). This is one-time, non-refundable payment, the monies received are non-tradeable and shouldn't be reflected on any trading account.
*   Users should be able to apply Promo codes which should give them a discount.
*   Backend needs to receive the following data to be able to add an account to the correct trading group and apply add-ons:
    *   Package ID
    *   Add-ons IDs
*   Upon successful purchase:
    *   for a fresh user: create new Quantum account,
    *   add account to the default trading group of a Package,
    *   adjust credits according to the Initial credits of the Challenge Settings,
    *   create a Challenge stats entry with a snapshot of Challenge Settings,
    *   adjust challenge parameters of the Challenge History record according to the purchased add-ons,
    *   set the Challenge status to New in the Challenge stats entry.
``````markdown
## Withdrawable Equity calculation

+ Change Withdrawable Equity calculation.

*   Withdrawals from the Quantum account should be allowed only when Traders' Profit Share > 0 in the Challenge definitions.
*   User can only Withdraw profits according to the Traders' Profit Share in the Challenge Definitions.

Current WD equity formula:

*   Withdrawable equity = Available funds - credits - [ Unrealized PL (when negative)]

WD equity formula for Quantum Accounts only:

*   Withdrawable equity = (Available funds - credits - [ Unrealized PL (when negative) ]) \* Traders' Profit share

**Example 1: negative PL**

*   User was given a funded account with 5000 credits.
*   User generated profits of 200: Available funds = 5200
*   User has open positions and PL = -50
*   Traders' profit share = 80%
*   Withdrawable Equity = (5200 - 5000 - (-50)) \* 0.8 = 120

**Example 2: positive PL**

*   User was given a funded account with 5000 credits.
*   User generated profits of 200: Available funds = 5200
*   User has open positions and PL = 50
*   Traders' profit share = 80%
*   Withdrawable Equity = (5200 - 5000 ) \* 0.8 = 160
``````markdown
## Challenge Settings

Global Challenge settings represent the base parameters that control ongoing challenges.

| Field                   | Type, Validation            | Comment                                                                                             |
| :---------------------- | :------------------------- | :-------------------------------------------------------------------------------------------------- |
| Challenge name          | String, required          | The challenge name to display on the challenge history pop up in the platform.                      |
| Label                   | Dropdown list, single choice, required | Default: blank                                                                                    |
| Profit target           | Required, float, 2 decimals, > 0 | A trading goal users must reach to successfully complete the challenge.                      |
| Trader Profit Share     | Required, float, 2 decimals, >= 0 | A share of generated profit users are allowed to withdraw. 0 means no profit split, i.e. users can't withdraw anything. |
| Reward Type             | Required, 0 - Payout, 2 - None | Default: 0                                                                                               |
| Daily Loss              | Required, float, 2 decimals, > 0 | A loss threshold that must be checked on every unrealized PL change. When reached, the challenge fails. |
| Max loss                | Required, float, 2 decimals, > 0 | A loss threshold that must be checked on every available funds change. When exceeded, the challenge fails. |
| Loss alert level        | Required, float, 2 decimals, >= 0 | A loss alert threshold that must be checked on every unrealize PL change. When reached, the notification should go out to the user. |
| Minimum Trading Days    | Required, integer, >= 0  | Trading day is any when user had opened positions. The challenge evaluation only happens when the actual trading days >= minimum trading days. |
| Inactivity Period (days) | Required, integer, >= 0  | The maximum number of days during which users are allowed to not have any open positions. If exceeded, the challenge fails. 0 means there's no inactivity check. |
| Initial credits         | Required, float, 2 decimals, > 0 | The amount of credit to add to a fresh Quantum account upon adding to the group. |
| Withdrawals delay (days) | Required, integer, >= 0  | Default: 5. The number of days after unlocking withdrawals the system should not allow withdrawals.                                                       |
| Margin coefficient      | Required, float, 2 decimals, > 0 | Default: 1  [Margin coefficient](https://www.example.com) |
| Weekend trading         | Checkbox                  | Default: unchecked. When enabled, challenges fail if user leaves open positions over weekend.   |
| News trading            | Checkbox                  | Default: unchecked. When disabled, the risk scoring should check whether user had open positions during the news events.   |
| Allowed profit sharing | Checkbox                  | Default: unchecked. When disabled, Trader Profit share value should be ignored and user should not be allowed to withdraw profits. |

## Add New Challenge

*   **Challenge name**
*   **Label**
*   **Profit target (%)** : 10.00
*   **Trader Profit Share (%)** : 80.00
*   **Daily loss (%)** : 5
*   **Max Loss (%)** : 8
*   **Loss alert level (%)** : 0
*   **Minimum trading days** : 0
*   **Inactivity period** : 0
*   **Initial credits** : 5000.00
*   **Withdrawals delay (da)** : 5
*   **Margin coefficient** : 1
*   **Reward Type** : Payout
*   **✔ Weekend trading**
*   **News trading**
*   **Allow profit sharing**

    [Cancel] [Add]

All fields are required.

**Additional validations:**

*   If **Trader Profit share > 0** and **Allow profit share** is checked, there should be a warning popup displayed: _Please note: Trader Profit share is ignored when Allow profit sharing is ticked._

This message should not block saving changes, it's just for user's information.

## Global and User-level challenge settings

Similarly to TD/GTD:

*   **Global Challenge settings** represent the settings on a Trading Group level.
*   **User-level Challenge Settings** represent the settings applicable to specific users.

**Example:**

*   **Global Challenge settings:**
    *   Profit target: 10%
    *   Daily loss: 5%
    *   Max loss: 8%
    *   Min trading days: 5
    *   ...other parameters
*   **User-level Challenge settings:**
    *   <Global Challenge Settings>
    *   Profit target: 15% - user purchased and add-on that overrides Profit target value

User-level Challenge settings do not necessarily need to be created for each and every trading account. Example: if a package allows to purchase 7 addons (each changes only one parameter), then there can be only 127 distinct combinations. So, in terms of storage efficiency, it makes sense to create User-level changes only when an end user purchases a combination of add-ons that doesn't yet a User-level Challenge settings matching record.

Each Quantum account should reference a single User-level Challenge settings variant at a time. And vice-versa, the same User-level Challenge settings variant may be referenced by multiple Quantum Accounts.
``````markdown
## Overview

To start with Prop Trading account users can purchase one of offered packages. Each package can have one or multiple challenges.
For example, a package can include 2 challenges:

*   Evaluation stage - at this stage user must hit the profit and min trading days target while staying within risk thresholds according to Challenge Settings. User is not eligible to withdraw profits at this stage.
*   Funded account - same as Evaluations stage but user is allowed to withdraw his profit share after hitting the profit target.

When Evaluation stage starts, user is given a Quantum account with credit amount according to Challenge Settings. In case if user hits the profit and min trading days targets of the Evaluation stage, the user is granted a Funded account (i.e. next challenge starts for the user automatically):

*   All positions are closed automatically.
*   User account moves to the Funded account trading group.
*   Available funds are adjusted according to Challenge Settings of the Funded account challenge.

When user fails to stay within the risk thresholds on any stage, the challenge fails:

*   All positions are closed automatically.
*   Further trading is disallowed.

User can purchase a new challenge and in such case the process starts over. However, user can't purchase a new challenge while already running another challenge.
User should be able to purchase an add-on during an ongoing challenge.

### Entity mapping

*   A Package can have one or multiple challenges and multiple add-ons available for users to purchase.
*   Challenges are defined by Global Challenge Settings, User-level Challenge Settings, Challenge History, and Add-ons:
*   Global Challenge settings are the base settings
*   User-level Challenge Settings are the base settings adjusted according the add-ons purchased by users.
*   Add-ons are the specific values that override the base Challenge Settings parameters.
*   Challenge history stores ongoing challenge statistics.

```
[Image of Entity relationship diagram]
```

### Business logic flowchart

The below diagram combines the following processes:

*   Sign-up and Purchasing packages
*   Trading
*   Withdrawals

```
[Image of Business Logic Flowchart]
```
```
→
→
Close all positions
↑
Set challenge
---
Decline WD
→ Approve WD
→
```
```markdown
## Withdrawals

Withdrawal process starts upon user request and includes the following steps:

*   Check whether the user has open positions or not.
*   Set the Challenge state to WDRequest or Decline the request.
*   Calculate risk score
*   Approve wd request is the score is ok, otherwise decline the request and fail the account.
*   Resume quantum session after processing WD request.

```mermaid
graph LR
    A[User sends WD request] --> B{has open positions?}
    B -- Yes --> C{Set challenge state to WDRequest, finish Quantum session}
    C --> D{Calculate risk score, review user account manually (if needed)}
    D --> E{risk score is ok?}
    E -- Yes --> F[Approve WD request]
    F --> G{Purchase process}
    E -- No --> H{Decline WD request}
    H --> I{Set challenge state to Failed, finish Quantum session}
    B -- No --> J{Decline WD request}
    J --> I

```

When user creates a request, the Withdrawable equity should be calculated according to the Profit share parameter of Challenge Definitions.

Users shouldn't be allowed to create WD requests unless the Challenge state is
``````markdown
## BO UI updates

*   **Add view-only Challenge History field to Portfolio | Retention tools** -> Back Office - Dealing
    The new section name: Challenges

    The section should display the most recent challenge history:

    *   all fields of the Challenge History record,
    *   User-level Challenge History settings variant fields,
    *   a dropdown field where BO user can select one of the past challenges.

    ![Image of the challenge history section]
    

*   **Add Package, Challenge Status and Challenge to search forms**

    *   Add Package, Challenge Status and Challenge to the search form.
    *   Challenge status drop-down field should display the all possible states: New, Active, Success, WDUnlocked, Failed.
    *   Challenge should list all available challenge names depending on the selected Label.
    *   Package should list all available package names depending on the selected Label.
    *   Add Package, Challenge State and Challenge to the results view as optional columns, hidden by default.

    **Dealing \ User management**

    ![Image of the search form with highlighted sections]

    **CRM | Advanced Search**

    *   First Name
    *   Surname
    *   Labels
    *   User Management
    *   User Type\*
    *   User ID
    *   Email
    *   Offices
    *   Teams
    *   Account Type
    *   Package
    *   Clear all
    *   Username
    *   Account ID
    *   User Status
    *   Desks
    *   External ID
    *   Currency
    *   Trading Platform
    *   Challenge
    *   Challenge state

---

*   **Add fields to CRM | Account search**
    ![Image of the CRM account search form]

*   **Add fields to CRM | Lead search**
    ![Image of the CRM lead search form]

*   **Add Challenge filter to the Positions and Entry Orders search**
    *   Challenge should list all available challenge names depending on the selected Label.
    ![Image of the Positions & Entry Orders Search form]

    **Positions & Entry Orders Search**

    **Positions Entry Orders**

    *   General
    *   Labels
    *   Status
    *   Amount
    *   Teams
    *   Symbol
    *   Desks
    *   Offices
    *   Symbol Type
    *   Date
    *   Open Date
    *   Close Date
    *   Cancel Date
    *   Ex Date
    *   Other
    *   User ID
    *   Search
    *   Clear all
    *   Position ID
    *   Challenge
    *   Calculate open positions P&L

*   **Add Challenge filter to Portfolio | Dealing | Closed positions**
    *   Challenge should list all challenge names that the end user participated in.
    ![Image of the Closed positions form]

---
```
```markdown
# Challenge Success and Fail Criteria Evaluation

## Challenge Fail Criteria:

*   Daily Loss
*   Max Loss
*   Inactivity period

## Channel Success Criteria:

*   Target profit
*   Minimum trading days

## Daily Loss and Max Loss

*   Daily Loss and Max Loss must be evaluated in real time updating on unrealized PL and available funds change.

### Examples:

**Case 1: Fresh account, no open positions, no closed positions:**

*   Initially Available funds = 5000
*   Daily Loss = 5%
*   Max Loss = 8%
*   Initial Daily Loss threshold = 5000 \* 0.05 = 250
*   Initial Loss threshold = 5000 \* 0.08 = 400

**Case 2: Few positions are open and losing (negative PL):**

*   Available funds = 4800
*   Daily Loss = 5%
*   Unrealized PL = -180
*   Realized PL = -20 (commission for opening a trade)
*   Current Daily Loss = Unrealized PL + Realized PL = -200
*   Daily Loss threshold = Initial Daily Loss threshold = 250
*   Daily Loss can't drop below the initial level:
    *   Available funds \* 0.05 = 240
    *   240 < Initial Daily Loss threshold
    *   Using Initial Daily Loss threshold to evaluate loss level
*   Max Loss threshold = Initial Realized Loss threshold = 400
*   Similarly to Daily Loss threshold: Realized Loss can't drop below the initial level

The challenge must fail when `abs(Current Loss) >= Daily Loss threshold` only if `Current Daily Loss < 0`.

The challenge must fail when `abs(Max Realized Loss) >= Max Realized Loss threshold` only if `Max Realized Loss < 0`.

**Case 3: Positions opened earlier generated some profit and user closed them.**

*   Available funds = 5200
*   Daily Loss = 5%
*   Max Loss = 8%
*   Daily Loss threshold = Available funds \* 0.05 = 260
*   Max Loss threshold = Available funds \* 0.08 = 416

## Inactivity Period

*   Inactivity period is the number of full calendar days a Quantum Account didn't have any trading activity. Inactivity period is defined in the Quantum Trade Group settings.

A calendar day counts as a day with no trading activity in case if the following conditions are met:

*   User didn't open new positions during a calendar day.
*   User didn't place any entry orders during a calendar day.
*   User didn't have any open positions during a calendar day.
*   User didn't have any pending entry orders during that day.

Inactivity period starts from the last closed position time or EO cancellation (including due to the EO expiration).

Swaps and other charges do not qualify as trading activity.

A trading activity is opening a position or placing EO.

The evaluation logic:

*   If Account doesn't have open positions and Account doesn't have active EO:
    *   If last trading activity time <= (last trading activity time + Inactivity Period (days)):
        *   Fail the challenge.
        *   Disable trading on the account.

## Target Profit and Minimum Trading Days

*   Minimum trading days is the number of days user performed any trading activity on the Quantum Account. See trading activity definition above. Minimum trading days criteria is defined in the Quantum Trading Group. Days when a user was inactive do not count when evaluating Minimum trading days.

*   Target profit criteria must be evaluated based on closed PL only. Unrealized PL is not taken into account even if the unrealized profit exceeds the target profit. Users must close positions before the Target profit evaluation takes place.

Target profit evaluation logic:

*   Target profit (%) = 10%
*   Initially Available fund = 5000
*   Target profit amount = 5000 \* 0.1 = 500
*   Target Available funds = 5500 or more
``````markdown
# Add-ons

Add-ons can be purchased by users with packages. Initially, business wants the following add-ons available:

*   **Double Leverage**
    *   Overrides Margin Coefficient in Challenge Definitions
*   **Higher Profit Share**
    *   Overrides Profit share in Challenge Definitions
*   **Hybrid max loss / profit target**
    *   Overrides Profit target and Max loss in Challenge Definitions.
*   **No Minimum Trading Days**
    *   Sets Minimum trading days to 0 in Challenge definitions.
*   **Trader Payouts 3 days guarantee**
    *   Overrides the min trading of days in Challenge Definitions.
*   **Weekend trading**
    *   Overrides the weekend trading flag in Challenge Definitions.
*   **News trading**
    *   Overrides the news trading flag in Challenge Definitions.

## + Add Add-ons administration UI to Backoffice Administration / Packages

![Add-ons administration UI](https://i.imgur.com/6e6V9f1.png)

*   Depending on the selected Add-on type, the following fields should be displayed:

![Package editing form](https://i.imgur.com/yK07zD3.png)

*   Enabled add-ons should be displayed in the Package editing form.
*   Since every add-on requires implementation, adding Add-ons from UI is not needed.

## Validations on saving changes:

*   if the current addon is selected in one of the enabled packages:
    *   show error message: *This addon can't be disabled because it's used by one of the enabled packages.*
``````markdown
## Setting up Packages, Challenges and Add-ons

The process of setting up the system for Prop Trading includes the following steps exactly in this order:

1.  (Optional) Create a Brand and/or a Label.
2.  Create a **Default Trading Group** with **Account type** set to **Profit | Quantum**.
3.  Create **Global Challenge Settings** for all challenge all packages.
4.  Create **Add-ons**
5.  Create **Packages**, add **Challenges** and **Add-ons**

**Important notes:**

*   Quantum Groups for the Prop trading product shouldn't have any limit on Exposure in GTD.
*   Parent label to a Quantum Group, shouldn't have any **Manual Cap**, **Quarterly commission**, and **Credit expiration**.
``````markdown
Trading

The system needs to monitor the following:

*   **On position open**
    *   Calculate the Initial margin considering margin coefficient taken from the User-level Challenge settings. [Margin coefficient](https://example.com/margin_coefficient) [Challenge settings](https://example.com/challenge_settings)
    *   According to the challenge fail criteria [Challenge success and fail criteria evaluation](https://example.com/challenge_success_fail)
        *   if failed: set Challenge state to Failed, close all positions, finish quantum session
*   **On unrealized PL change**
    *   According to the challenge fail criteria
        *   if failed: set Challenge state to Failed, close all positions, finish quantum session
*   **On Position close**
    *   According to the challenge success or fail criteria
        *   if failed: set Challenge state to Failed, close all positions, finish quantum session
        *   if successful:
            *   if the next challenge is specified in the challenge definitions
                *   set Challenge state a Success
                *   close all positions,
                *   move account to another trading group according to the challenge definitions,
                *   create new Challenge stats record
                *   adjust credits to meet the Challenge definitions of the next challenge
                *   set Challenge state to Active
                *   send notifications [Notifications](https://example.com/notifications)
            *   if there isn't next challenge specified
                *   Keep Challenge state as Active
                *   send notifications
*   **On EOD**
    *   Update Elapsed trading days of the [Challenge History](https://example.com/challenge_history)
    *   If user have not opened any positions during the Inactivity period according to the User-level Challenge settings, set Challenge status to Failed, finish quantum session.

Section 4

```
Purchase
process
Set Challenge
status to Failed,
liquidate account,
remove credits,
finish Quantum
Close all positions,
finish Quantum
WD process
Session
session
↑
个
no next challenge
Fail
User opens first
position
Monitor challenge
success/fail
criteria, set
challenge status
to Active when
user starts trading
next
Success >
challenge
Set challenge state
to Success
Add Initial credits
Create new
Challenge history
record
Challenge status:
New
```
```markdown
## Packages

Package is a logical container for challenges. A package offers one or multiple challenges. Challenge settings can be overridden by Add-ons.

| Parameter              | Type, validation       | Comment                                  |
| ---------------------- | ---------------------- | ---------------------------------------- |
| Package Name           | non-empty string       |                                          |
| Package Description    | non-empty string       |                                          |
| Brand                  | Dropdown, single choice, required |                                          |
| Label                  | Dropdown, single choice, required |                                          |
| Trading group          | Dropdown, single choice, required |                                          |
| Learn more link        | string                 |                                          |
| Available from         | date                   |                                          |
| Available until        | date                   |                                          |
| Leverage               | Dropdown, single choice, required | same as MaxLeverage on GTD.                 |
| Initial balance (USD)  | float, 2 decimals, >=0 |                                          |
| Full price             | float, 2 decimals, >=0 |                                          |
| Discounted price       | float, 2 decimals, >=0 |                                          |
| Daily loss             | float, 2 decimals, >=0 |                                          |
| Max loss               | float, 2 decimals, >=0 |                                          |
| Minimum trading days   | integer, >=0           |                                          |
| Add-ons                | Checkbox group         | List of AddonsIds (see Add-ons)        |
| Challenges             | List of ChallengeSettingsIDs | User should be able to select challenges and add them to the list. |

---

### Add New Package

Visible
*   **Package name**
*   **Package description**
*   **Brand**
*   **Label**
*   **Trading group**
*   **Available from**: 01/08/2025
*   **Available until**: 01/09/2025
*   **Leverage**: 1:30
*   **Initial balance**: 0
*   **Full price**: 100.00
*   **Discounted price**: 100
*   **Daily loss %**: 5
*   **Max loss %**: 20
*   **Min trading days**: 5
*   **Learn more**

**Add-ons**
*   Higher profit share
*   Double leverage
*   Hybrid max loss / profit target
*   No minimum trading days

**Challenges**

| Position | ID       | Group Challenge         |   | X   | Delete |
| :------- | :------- | :----------------------- | - | -   | ------ |
| 1        | 45353454 | Quantum challenge 2    |   |       |        |
| 2        | 456696959 | Quantum challenge 3    |   |       |        |
| 3        | 456696959 | Quantum challenge 3    |   |       |        |

+   Add Challenges
  X Delete
Cancel
Add

*   All fields are required, except for Add-ons.
*   Challenges list displays challenges added to the package manually. Challenges can be reordered. The order in the list defines the order users will take challenges.

**+ Permissions for Package Admin**
*   view prop trading - should be automatically granted to all users who can view Administration sector
*   edit prop settings - allows to add and edit packages, views, and add-ons, and should be granted on demand.
*   delete prop settings - allows to delete packages, views, and add-ons, can not be granted without the edit permission.
``````markdown
# Challenge History

Challenge History is an entity that represents an ongoing or completed challenge state.

| Field                | Allowed values | Comment                                                                                                                                                                                                  |
| -------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Max Daily Loss amount | float          | Based on the currently available funds but not less than the initial Max Daily Loss amount. Updates on available funds change or when User purchases another add-on during the challenge.                |
| Max Loss amount      | float          | Based on the currently available funds but not less than the initial Max Loss amount. Updates on available funds change or when User purchases another add-on during the challenge.                     |
| Elapsed trading days | integer        | The number of days counted as active trading days. Updates on EOD according to the definition of trading activity or when User purchases another add-on during the challenge. See [Challenge success and fail criteria evaluation](https://www.example.com) |
| Inactive trading days | integer        | The number of days counted as inactive trading days. Updates on EOD according to the definition of trading activity.                                                                                 |
| Package name         |                | For display purposes. Updates once on creating a Challenge History record.                                                                                                                                |
| Add-ons              |                | For display purposes. Updates once on creating a Challenge History record or when User purchases another add-on during the challenge.                                                                      |
| Challenge status     | 0 - New<br>1 - Active<br>2 - Success<br>3 - Failed<br>4 - WDUnlocked  | Indicates the current status of user's challenge. See Challenge status model below.                                                            |
| FailReason           | 0...3 (see descriptions below) | Default: blank. For display purposes. Indicates why the challenge failed.                                                                                                            |

Each Challenge History record should reference a User-level challenge setting variant (see Challenge settings ) as well as the the following data:

Challenge fail reasons:

*   Weekend trading not allowed.
*   Your loss exceeded max loss threshold.
*   Your loss exceeded daily loss threshold.
*   Challenge failed due to inactivity.

Each Challenge History record should reference one Quantum Account.

Case 1: User purchased a package and starts trading

*   New Challenge history record is created and gets Active status.

Case 2: The same user failed a challenge and purchased another package.

*   The Challenge history record from Case 1 get Failed status
*   New Challenge history record is created and gets Active status.

Case 3: The same user successfully completed an evaluation stage challenge and got a funded account challenge.

*   The active Challenge history record from Case 2 gets status Success.
*   New Challenge history record is created and gets Active status.

This way the history of all user challenges is preserved.

## Challenge status model

Challenge lifecycle includes the following states:

*   **New** - a new challenge, Quantum session is started, but no position/EO has been opened.
*   **Active** - user has opened at least one position or placed at least on EO.
*   **Success** - user hit the profit and min trading days targets.
*   **Failed** - user exceeded risk thresholds. Quantum session is stopped, all positions are closed, EO are canceled.
*   **WDUnlocked** - user is eligible to request withdrawals.

```mermaid
graph LR
    New --> Active
    Active --> Success
    Active --> Failed
    Success --> WDUnlocked
    WDUnlocked --> Failed
    Failed -- (Final State) --> |No Change| Failed
```

New → Failed transition happens when a user purchased a package but didn't open any positions and didn't placed any EO during the Inactivity period.

New → Active transition happens when user starts trading (open position or place EO).

Active → Failed transition happens when user fails to stay within risk thresholds according to the Challenge Definitions.

Active → Success transition happens when user hits profit and min trading days targets and the next challenge is specified in the Challenge Definition.

Active → WDUnlocked transition happens when user hits profit and min trading days targets and the next challenge is not specified in the Challenge Definition.

WDUnlocked → Failed transition happens when user fails to stay within risk thresholds according to the Challenge Definitions.

Failed is a final status. Once the Challenge failed, no changes can be made to it.
``````markdown
## Notifications

In-app notifications and email messages:

| Notifications                                                        | Comment                                                                                                                                           |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| **• Trigger:** Create new challenge                                 |                                                                                                                                                   |
| **• Title:** New challenge started                                   | The payload data should be taken from Challenge definitions, either from Trading Group or from user level.                                            |
| **• Body:**                                                         | `challenge_name`, `profit_value`, `daily_loss`, and `max_loss` should be in USD                                                                  |
| &nbsp;&nbsp;&nbsp; Challenge: {{challenge\_name}}                  |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Target profit: {{profit\_value}}                 |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Daily loss: {{daily\_loss}}                     |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Max loss: {{max\_loss}}                         |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Min Trading Days: {{min\_trading\_days}}          |                                                                                                                                                   |
| **• Trigger:** Set challenge state to Failed due challenge exceeding daily loss. | Payload values:                                                                                                                                  |
| **• Title:** Challenge failed                                        | For `current_loss` and `daily_loss` calculations see [Challenge success and fail criteria evaluation](<#Link_to_Challenge_success_and_fail_criteria_evaluation>) |
| **• Body:**                                                         |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; {{fail\_reason}}                                   | `fail_reason` is available in Challenge stats entry  [Challenge History](<#Link_to_Challenge_History>)                                         |
| &nbsp;&nbsp;&nbsp; Current loss: {{current\_loss}}                  |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Max Daily loss: {{daily\_loss}}                  |                                                                                                                                                   |
| **• Trigger:** Set challenge state to Failed due to exceeding max loss. | Payload values:                                                                                                                                  |
| **• Title:** Challenge failed                                        | For `current_loss` and `max_loss` calculations see [Challenge success and fail criteria evaluation](<#Link_to_Challenge_success_and_fail_criteria_evaluation>) |
| **• Body:**                                                         |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; {{fail\_reason}}                                   | `fail_reason` is available in Challenge stats entry [Challenge History](<#Link_to_Challenge_History>)                                          |
| &nbsp;&nbsp;&nbsp; Current loss: {{current\_loss}}                  |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Max loss: {{max\_loss}}                         |                                                                                                                                                   |
| **• Trigger:** EOD friday (if Weekend trading add-on has been purchased). | `fail_reason` is available in Challenge stats entry [Challenge History](<#Link_to_Challenge_History>)                                          |
| **• Title:** Challenge failed                                        | For `current_loss` and `max_loss` calculations see [Challenge success and fail criteria evaluation](<#Link_to_Challenge_success_and_fail_criteria_evaluation>) |
| **• Body:**                                                         |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; {{fail\_reason}}                                   |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Current loss: {{current\_loss}}                  |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Max loss: {{max\_loss}}                         |                                                                                                                                                   |
| **• Trigger:** Set challenge state to Success                        | `challenge_name` should be taken from Challenge definitions.                                                                                 |
| **• Title:** Challenge completed!                                  |                                                                                                                                                   |
| **• Body:**                                                         | `profit_value` = Available funds - Initial funds                                                                                                  |
| &nbsp;&nbsp;&nbsp; Congratulations! You have successfully completed the challenge:                                       |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; {{challenge\_name}}                               |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Profit: {{profit\_value}}                        |                                                                                                                                                   |
| **• Trigger:** beginning of the trading day                          | This notification should be sent daily.                                                                                                            |
| **• Condition:** Challenge state == Active \|\| Challenge state == WDUnlocked | `trading_day` is a counter of trading days elapsed.                                                                                   |
| **• Title:** Challenge status                                         |                                                                                                                                                   |
| **• Body:**                                                         |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Trading day: {{trading\_day}}                     |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Actual Equity: {{actual\_equity}}              |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Profit: {{profit}}                              |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Target profit: {{target\_profit}}                |                                                                                                                                                   |
| **• Trigger:** Current loss has reached the Loss alert level.        | `daily_loss` should be in USD                                                                                                                  |
| **• Title:** Loss alert!                                           |                                                                                                                                                   |
| **• Body:**                                                         |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Your loss is dangerously close to the Daily loss threshold. |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Max daily loss: {{daily\_loss}}                  |                                                                                                                                                   |
| **• Trigger:** Set challenge state to WDUnlocked                    |                                                                                                                                                   |
| **• Title:** Withdrawals unlocked!                                  |                                                                                                                                                   |
| **• Body:**                                                         |                                                                                                                                                   |
| &nbsp;&nbsp;&nbsp; Congratulations! You can now withdraw your profits!     |                                                                                                                                                   |
```
```markdown
## Quantum account creation

Quantum accounts are created upon signup and should be added to the default trading group.

Default trading group should be taken from Label.

- Quantum Session must be disabled by default.
- Billing definitions on user level must be overridden:
    - Allow deposit must be set to False.
``````markdown
# Prop BO UI updates

1.  Combine packages, challenges, and add-ons into one section under Administration:

    **Prop trading:**

    *   Packages
    *   Challenges
    *   Add-ons

    Packages and Add-ons views and forms are ok as they add. Please add the view for challenges.

    **Challenges**

    | Label          | Group            | Initial credits | Daily loss | Max loss | Min trading days | Target profit | Profit share |
    | :------------- | :--------------- | :-------------- | :--------- | :------- | :--------------- | :------------ | :----------- |
    | A3Trading      | A3Trading_ES)eval | 10,000.00       | 5%         | 8%       | 4                | 10%           | 90%          |
    | A3Trading      | A3Trading_ES_funded | 10,000.00       | 5%         | 8%       | 4                | 10%           | 80%          |

    Update the Challenge add/edit form. New fields:

    *   Label
    *   Group
    *   Margin coefficient
    *   Weekend trading
    *   News trading

    Remove `Daily loss behavior` field.

    ---

    **New Challenge**

    | Field                    | Example Value |
    | :----------------------- | :------------ |
    | Label \*                 | TradeApp      |
    | Group \*                 | TradeApp_evaluation |
    | Profit target (%)\*        | 10.00         |
    | Trader Profit Share (%) \* | 80.00         |
    | Reward type \*             | Payout        |
    | Daily loss (%) \*        | 5             |
    | Max loss (%) \*          | 8             |
    | Loss alert level (%) \*    | 4             |
    | Minimum trading days \*    | 0             |
    | Inactivity period (days) \* | 5             |
    | Initial credits \*         | 5000.00       |
    | Withdrawals delay (days) \* | 5             |
    | Margin coefficient \*      | 1             |
    | Weekend trading          | [checkbox]    |
    | News trading             | [checkbox]    |

    Next challenge:

    | Id  | Group                |
    | :-- | :------------------- |
    | 123 | Quantum challenge 2  |
    | 123 | Quantum challenge 3  |
    |     | <Clear Selection button> |

2.  Remove `Challenge definitions` tab from Trading Group.
3.  Remove `Challenge definitions` tab from Dealing Portfolio.
4.  Add challenge parameters to Portfolio | CRM | Retention tools:  Back Office - Dealing

    Challenge parameters should be the same as New challenge form except fields should be view only.
```