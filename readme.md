# InsiderOne QA Automation Case


Automation solution for the **InsiderOne QA job listings test case** implemented using **Python, Selenium, Pytest and Page Object Model (POM)**.

---

# Technologies

- 🐍 Python  
- 🌐 Selenium WebDriver  
- 🧪 Pytest  
- 🧱 Page Object Model (POM)  
- 🔧 WebDriver Manager  

---

# Test Scenario

The automation validates the following workflow:

1. Open the **Insider homepage**
2. Navigate to the **Quality Assurance careers page**
3. Click **See all QA jobs**
4. Verify the **Department filter is preselected as "Quality Assurance"**
5. Filter jobs by **Location: Istanbul, Turkiye**
6. Validate that job listings contain:
   - **QA / Quality Assurance** in the title
   - **Department: Quality Assurance**
   - **Location: Istanbul, Turkiye**
7. Click **View Role**
8. Verify redirection to the **Lever application page**
9. Validate job details on the job detail page:
   - Title contains **QA**
   - Department **Quality Assurance**
   - Location **Istanbul, Turkiye**

---

# Project Structure

```
pages/
 ├── BasePage.py
 ├── HomePage.py
 └── JobsPage.py

tests/
 └── test_case.py

utils/
 └── driver.py

conftest.py
pytest.ini
requirements.txt
README.md
```

---

#Run Tests

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run tests

```bash
pytest -v
```

---

#Notes

- The project follows the **Page Object Model (POM)** design pattern.
- **Explicit waits** are used to handle dynamic page loading.
- The test handles **new tab navigation** when opening the Lever application page.
- A **screenshot is captured automatically if a test fails**.

---

# Author

**Berkay Selbes**
