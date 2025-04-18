# Generated by Phi-2 via Ollama

class Solution:
    # Solution in Python 3
    class Solution:
        def maxProfit(self, prices) -> int:
            # Initialize variables to store the minimum price and maximum profit
            min_price = float('inf')
            max_profit = 0
            # Loop through the prices list
            for i in range(len(prices)):
                # Update the minimum price if the current price is lower than the previous minimum price
                if prices[i] < min_price:
                    min_price = prices[i]
                # Calculate the profit by subtracting the minimum price from the current price
                profit = prices[i] - min_price
                # Update the maximum profit if the current profit is higher than the previous maximum profit
                if profit > max_profit:
                    max_profit = profit
            return max_profit
