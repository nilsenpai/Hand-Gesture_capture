# Real-Time Hand Gesture Recognition

**Author**: Soumanil Sarkar  
**Assignment**: AI Intern Assessment – Real-Time Static Hand Gesture Recognition  

## ✋ What it Does
- Recognizes 4 gestures in real-time using webcam:
  - Open Palm
  - Fist
  - Peace (✌️)
  - Thumbs Up (👍)

## ⚙️ How to Run
```bash
git clone https://github.com/yourusername/hand-gesture-recognition.git
cd hand-gesture-recognition
pip install -r requirements.txt
python main.py
Press **q** to quit.

## 🛠️ Tech Used
- **MediaPipe** → for detecting hand landmarks  
- **OpenCV** → for webcam + drawing  
- **NumPy** → small math helpers  

## 🧠 Gesture Logic
- **Fist** → no fingers up  
- **Open Palm** → 4 or more fingers up  
- **Peace** → index + middle up, others down  
- **Thumbs Up** → thumb up, others folded  

## 🎥 Demo


https://github.com/user-attachments/assets/4b75d92b-022b-4035-a02a-d236bff4ec6f


