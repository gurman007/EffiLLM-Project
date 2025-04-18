# Generated by Gemma 2B via Ollama

class Solution:
    defrussianDoll(self, envelopes):
        """
        :type envelopes: List[List[int]]
        :rtype: int
        """
        # Initialize a dictionary to store the maximum height and width for each width
        max_width_height = {}
        max_num_envelopes = 0

        # Iterate over the envelopes
        for width, height in envelopes:
            # Check if the current envelope can fit into the existing largest envelope
            if width <= max_width_height.get(width, 0) and height <= max_width_height.get(height, 0):
                # Increment the number of envelopes and update the maximum height and width
                max_num_envelopes += 1
                max_width_height[width] = max(height, max_width_height.get(width))

        return max_num_envelopes

