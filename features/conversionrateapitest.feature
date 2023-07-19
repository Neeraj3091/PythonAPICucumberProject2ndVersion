# Created by 364505 at 04.05.2023
Feature: Automation Testing Task to Test Base Currency API
  Returns real-time exchange rate data updated every 60 minutes, every 10 minutes or every 60 seconds.

  Scenario: Verify API return status code 200 and execute successfully with valid API key
    Given the API endpoint is "https://api.apilayer.com/fixer/latest"
    When I request the conversion rate
    Then the API should be up and return status code 200

  Scenario: Verify API is takes EUR as base by default
    Given the API endpoint is "https://api.apilayer.com/fixer/latest"
    When I request the conversion rate
    Then the response generated takes EUR as default base currency

  Scenario: Verify API returns status code 401 Unauthorized in case of invalid API key
    Given the API endpoint is "https://api.apilayer.com/fixer/latest"
    When I request the conversion rate with invalid API key
    Then the API should return status code 401
    And it should return message as "Invalid authentication credentials"

  Scenario Outline: Verify API returns only conversion rate between base(EUR) and symbols(NOK)
    Given the API endpoint is "https://api.apilayer.com/fixer/latest"
    When I request the conversion rate for valid "<base>" and "<symbols>"
    Then the API should return result only for given input
    And the conversion rate for given symbols should not be empty or null
    Examples:
      | base |  | symbols |
      | EUR | | NOK |
      | INR | | USD |


  Scenario Outline: Verify API returns error message for invalid currency
    Given the API endpoint is "https://api.apilayer.com/fixer/latest"
    When I request the conversion rate for invalid "<base>" and "<symbols>"
    Then the API should return status as false and give appropriate message
    Examples:
      | base |  | symbols |
      | EUR | | XXX |
