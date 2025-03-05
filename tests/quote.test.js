// tests/quote.test.js
describe('Quote Display', () => {
    test('fetches and displays a quote successfully', async () => {
      // Mock fetch for testing (simulates API response)
      global.fetch = jest.fn(() =>
        Promise.resolve({
          json: () => Promise.resolve({ content: 'Success is no accident', author: 'Thomas Edison' }),
          status: 200,
        })
      );

      // Simulate fetching a quote
      const quote = await fetch('https://api.quotable.io/random?tags=motivational').then(res => res.json());
      expect(quote.content).toBe('Success is no accident');
      expect(quote.author).toBe('Thomas Edison');
    });

    test('handles API failure gracefully', async () => {
      global.fetch = jest.fn(() => Promise.reject(new Error('API failed')));
      await expect(fetch('https://api.quotable.io/random?tags=motivational')).rejects.toThrow('API failed');
    });
  });
