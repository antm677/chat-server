You will be provided with the following:

User Input: {user_input}

Instructions:

1.  Analyze the user input to identify the main question or request.
2.  Break down the main question into smaller, more specific sub-queries. These sub-queries should focus on terminology or specific questions related to product specifications stored in the RAG.
3.  Present the sub-queries as a string. Delimit sub-queries in the resulting string with `|||`.

Example:

User Input:
"What are the key features and specifications of the new XYZ Pro model, and how does it compare to the previous ABC model?"

Resulting string:
"What are the key features of the XYZ Pro model?"|||What are the specifications of the XYZ Pro model?|||What are the key features of the ABC model?||What are the specifications of the ABC model?|||How does the XYZ Pro model compare to the ABC model in terms of features and specifications?"
