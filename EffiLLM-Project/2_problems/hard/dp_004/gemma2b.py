# Generated by Gemma 2B via Ollama

class Solution:
    def sellingWood(self, m: int, n: int, prices: [[int, int, int]]) -> int:
        dp = [[[0] * (n + 1) for _ in range(m + 1)] for _ in range(n + 1)]

        # Initialize the first row and column
        for i in range(1, m + 1):
            dp[i][0] = prices[i - 1][1]

        # Initialize the first column
        for j in range(1, n + 1):
            dp[0][j] = prices[0][j - 1]

        # Calculate the maximum profit for each cell
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + prices[i - 1][2]

        return dp[m][n]

