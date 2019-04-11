def academYearsList(x,y,n):
    years = [(None,'Joining Year' if n==1 else 'Passout Year')]
    for value in range(x,y+1):
        years.append((value,(str(value))))
    return years

statesList = [(None,'Select State'),('Andaman and Nicobar','Andaman and Nicobar'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chattisgarh','Chattisgarh'),
    ('Dadar and Nagar Haveli','Dadar and Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Pondicherry','Pondicherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
]

softSkillsList=[('Communication','Communication'),('Decision making','Decision making'),
('Self-motivation','Self-motivation'),
('Time managment','Time managment'),
('Leadership','Leadership'),
('Conflict resolution','Conflict resolution'),
('Adaptability','Adaptability'),
('Team Work','Team Work'),
('Creativity','Creativity'),
('Problem Solving','Problem Solving'),
('Flexibility','Flexibility'),
('Organization','Organization'),
('Dependability','Dependability'),
('Commitment','Commitment'),
('Achievments','Achievments'),
('Integrity','Integrity'),
('Effective Planing','Effective Planing'),
('Computer & Technical Literacy','Computer & Technical Literacy'),
('Project Management Skills','Project Management Skills'),
('Strong Work Ethic','Strong Work Ethic'),
('Emotional Inteligence','Emotional Inteligence'),
]
skillLevels = [(None,'Select Skill Level'),('Beginner','Beginner'),('Intermediate','Intermediate'),('Expert','Expert')]

techSkillsList = [('Ux Design','Ux Design'),
('Artificial Intelligence','Artificial Intelligence'),
('Cloud Computing','Cloud Computing'),
('EXCEL','EXCEL'),
('Interactive Prototyping','Interactive Prototyping'),
('Computer Science Fundamentals','Computer Science Fundamentals'),
('Data Modeling','Data Modeling'),
('System Design','System Design'),
('Statistics & Probability','Statistics & Probability'),
('Technical Reporting','Technical Reporting'),
('Front-End Devolopment','ront-End Devolopment'),
('Back-End Devolopment','Back-End Devolopment'),
('Mobile Devolopment','Mobile Devolopment'),
('Network Structure & Security','Network Structure & Security'),
('Photo Shop','Photo Shop'),
('Branding','Branding'),
('Java','Java'),
('XMl','XMl'),
('C Language','C Language'),
('C++','C++'),
('JavaScript','JavaScript'),
('SQL','SQL'),
('HTML','HTML'),
('UML','UML'),
('Python','Python')]

degreesList = [(None,'Select Degree'),
('B.Arch','B.Arch'),
('B.A','B.A'),
('B.A.M.S','B.A.M.S'),
('B.B.A','B.B.A'),
('B.Com','B.Com'),
('B.C.A','B.C.A'),]