The Facial Surveillance System is designed to detect malicious activities in real time.
It monitors an individual’s attention based on the combined positions of their eyes and head.
When the system detects signs of inattention (e.g., the individual looking away from the camera), it sends alerts via pop-up warnings on the screen and email notifications to the relevant authority.

Different functions were used to identify facial positions and trigger warnings:
1. facial-marking.py: Identifies facial landmarks using the facemesh technique.
2. eye_pos.py: Extracts eye positions based on pixel counts.
3. head_pos.py: Estimates head rotation angles using Rodrigues' rotation formula.
4. alerts.py: Issues on-screen warning pop-ups and sends email alerts with snapshots of the individual.
5. main.py: Serves as the main component that integrates all functions to operate the surveillance system effectively.
