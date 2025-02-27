// tests/form.test.js
describe('Transaction Form Validation', () => {
    test('validates amount is greater than 0', () => {
      const isValid = (amount) => amount > 0; // Mock form validation logic
      expect(isValid(1000)).toBe(true);
      expect(isValid(-100)).toBe(false);
      expect(isValid(0)).toBe(false);
    });
  });