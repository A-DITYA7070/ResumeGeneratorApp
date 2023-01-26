# TABLES IN Resume App

user 
  - id
  - username

PersonalDetails
   - id
   - name
   - Phone
   - email
   - address
   - linkedin url
   - ForeignKey('user.id')

Projects 
   - id
   - name
   - desc
   - start_date
   - end_date
   - ForeignKey('user.id')

Experiences
   - id
   - company_name
   - role
   - role_desc
   - start_Date
   - end_date
   - ForeignKey('user.id')

Education
   - id
   - school_name
   - degree_name
   - start_Date
   - end_date
   - ForeignKey('user.id')

certificates:
   - id
   - title
   - start_Date
   - end_date
   - ForeignKey('user.id')

skills:
   - id
   - title
   - confidence_score
   - Foreign_key('user.id')