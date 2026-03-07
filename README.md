# Virtual Robot Simulation Project (Final Project)
# مشروع محاكاة الروبوت الافتراضي (المشروع النهائي)

This project is an implementation of a virtual autonomous robot in a 2D grid environment using Python. The robot can autonomously plan its path and navigate from a starting point to a goal, avoiding obstacles along the way.

هذا المشروع هو تطبيق لروبوت افتراضي مستقل يعمل في بيئة شبكية ثنائية الأبعاد باستخدام لغة بايثون. يستطيع الروبوت تخطيط مساره بشكل مستقل والتحرك من نقطة البداية إلى الهدف، متجنبًا العوائق في طريقه.

---

## English Section

### 1. Project Description

This program simulates a robot operating in a 2D world represented by a grid. The environment can contain obstacles, a starting point, and a goal. The robot's objective is to find the most efficient path to the goal and execute the movement. The project is built entirely in standard Python without external AI or robotics libraries, focusing on algorithmic thinking and object-oriented design.

### 2. Implemented Features

This project fulfills the core requirements and includes the following two extension tracks:

*   **Core Requirements:**
    *   **2D Environment:** A grid-based map with boundaries and obstacles.
    *   **Robot Model:** The robot has a position (`x`, `y`), a direction, and an internal state.
    *   **Movement System:** The robot can move forward and turn. It prevents collisions with obstacles defined in the initial map.
    *   **Decision-Making Logic:** The robot's logic is controlled by a Finite State Machine (FSM).
    *   **Simulation Loop:** The simulation runs step-by-step, updating the robot's state and position over time.

*   **Extension Tracks Implemented:**
    1.  **A. Path Planning (A\* Algorithm):** The robot uses the A\* algorithm to find the shortest path from its starting position to the goal, taking obstacles into account.
    2.  **C. Finite State Machine (FSM):** The robot's behavior is managed by a clear FSM with the following states:
        *   `PLANNING`: The robot calculates the path using A\*.
        *   `EXECUTING_PATH`: The robot follows the calculated path step-by-step.
        *   `FINISHED`: The robot has successfully reached the goal.
        *   `STUCK`: The robot could not find a path to the goal.

### 3. Explanation of Algorithms

#### A\* Pathfinding Algorithm

A\* (A-Star) is a pathfinding algorithm that efficiently finds the shortest path between two points. It works by evaluating nodes (grid cells) based on the formula: `F = G + H`.

*   `G`: The actual cost (number of steps) from the start node to the current node.
*   `H`: The heuristic, or estimated cost, from the current node to the end node. We use the **Manhattan Distance** for this, which is calculated as `|x2 - x1| + |y2 - y1|`.
*   `F`: The total estimated cost of the path through the current node.

The algorithm maintains an "open list" (a priority queue) of nodes to visit and a "closed list" of nodes already visited. In each step, it picks the node with the lowest `F` score from the open list and explores its neighbors, updating their scores if a better path is found. This process continues until the goal is reached.

#### Finite State Machine (FSM)

The FSM is the "brain" of the robot. It dictates the robot's behavior by transitioning between a set of predefined states. Our FSM works as follows:
1.  The robot starts in the `PLANNING` state. It calls the A\* algorithm to compute a path.
2.  If a path is found, it stores the path and transitions to the `EXECUTING_PATH` state. If not, it transitions to `STUCK`.
3.  In the `EXECUTING_PATH` state, the robot moves one step at a time along the stored path.
4.  Once the robot reaches the final coordinate in its path, it transitions to the `FINISHED` state, and the simulation ends.

### 4. Instructions to Run the Program

1.  **Prerequisites:** Make sure you have Python 3 installed on your system.
2.  **Save the Code:** Save the provided Python code in a file named `robot_simulation.py` (or any other `.py` name).
3.  **Run from Terminal:** Open a terminal or command prompt, navigate to the directory where you saved the file, and run the following command:
    ```bash
    python robot_simulation.py
    ```
4.  **Observe the Simulation:** The simulation will start running in the terminal. You will see the grid being printed at each step, with the robot (`^`, `>`, `v`, `<`) moving along the calculated path (`*`) towards the goal (`G`). The robot's current state will also be printed below the grid.

---

## القسم العربي

### ١. وصف المشروع

هذا البرنامج يحاكي روبوتًا يعمل في عالم ثنائي الأبعاد ممثل بشبكة. يمكن أن تحتوي البيئة على عوائق، نقطة بداية، وهدف. هدف الروبوت هو إيجاد المسار الأكثر كفاءة للوصول إلى الهدف وتنفيذ الحركة. تم بناء المشروع بالكامل باستخدام لغة بايثون القياسية دون الاعتماد على مكتبات خارجية للذكاء الاصطناعي أو الروبوتات، مع التركيز على التفكير الخوارزمي والتصميم كائني التوجه.

### ٢. الميزات المطبقة

هذا المشروع يحقق جميع المتطلبات الأساسية ويتضمن مساري التطوير التاليين:

*   **المتطلبات الأساسية:**
    *   **بيئة ثنائية الأبعاد:** خريطة قائمة على شبكة مع حدود وعوائق.
    *   **نموذج الروبوت:** للروبوت موضع (`x`, `y`)، اتجاه، وحالة داخلية.
    *   **نظام الحركة:** يمكن للروبوت التحرك للأمام والانعطاف. يمنع الاصطدام بالعوائق المحددة في الخريطة الأولية.
    *   **منطق اتخاذ القرار:** يتم التحكم في منطق الروبوت بواسطة آلة الحالة المحدودة (FSM).
    *   **حلقة المحاكاة:** تعمل المحاكاة خطوة بخطوة، محدثةً حالة الروبوت وموقعه مع مرور الوقت.

*   **مسارات التطوير المطبقة:**
    1.  **أ. تخطيط المسار (خوارزمية A\*):** يستخدم الروبوت خوارزمية A\* لإيجاد أقصر مسار من نقطة البداية إلى الهدف، مع الأخذ في الاعتبار العوائق.
    2.  **ج. آلة الحالة المحدودة (FSM):** تتم إدارة سلوك الروبوت بواسطة FSM واضحة تتضمن الحالات التالية:
        *   `PLANNING` (تخطيط): يقوم الروبوت بحساب المسار باستخدام A\*.
        *   `EXECUTING_PATH` (تنفيذ المسار): يتبع الروبوت المسار المحسوب خطوة بخطوة.
        *   `FINISHED` (انتهى): وصل الروبوت بنجاح إلى الهدف.
        *   `STUCK` (عالق): لم يتمكن الروبوت من إيجاد مسار إلى الهدف.

### ٣. شرح الخوارزميات

#### خوارزمية A\* لإيجاد المسار

A\* (A-Star) هي خوارزمية لإيجاد المسارات تجد بكفاءة أقصر مسار بين نقطتين. تعمل عن طريق تقييم العقد (خلايا الشبكة) بناءً على المعادلة: `F = G + H`.

*   `G`: التكلفة الفعلية (عدد الخطوات) من عقدة البداية إلى العقدة الحالية.
*   `H`: التكلفة التقديرية (Heuristic) من العقدة الحالية إلى عقدة النهاية. نستخدم هنا **مسافة مانهاتن**، والتي تُحسب كالتالي: `|x2 - x1| + |y2 - y1|`.
*   `F`: التكلفة الإجمالية التقديرية للمسار عبر العقدة الحالية.

تحتفظ الخوارزمية بـ "قائمة مفتوحة" (طابور أولوية) للعقد التي يجب زيارتها و"قائمة مغلقة" للعقد التي تمت زيارتها بالفعل. في كل خطوة، تختار العقدة ذات أقل قيمة `F` من القائمة المفتوحة وتستكشف جيرانها، محدثةً قيمهم إذا تم العثور على مسار أفضل. تستمر هذه العملية حتى يتم الوصول إلى الهدف.

#### آلة الحالة المحدودة (FSM)

آلة الحالة المحدودة هي "عقل" الروبوت. هي التي تملي سلوك الروبوت عن طريق الانتقال بين مجموعة من الحالات المحددة مسبقًا. تعمل FSM الخاصة بنا كالتالي:
1.  يبدأ الروبوت في حالة `PLANNING`. يستدعي خوارزمية A\* لحساب المسار.
2.  إذا تم العثور على مسار، يقوم بتخزينه وينتقل إلى حالة `EXECUTING_PATH`. إذا لم يجد، ينتقل إلى حالة `STUCK`.
3.  في حالة `EXECUTING_PATH`، يتحرك الروبوت خطوة واحدة في كل مرة على طول المسار المخزن.
4.  بمجرد وصول الروبوت إلى الإحداثي الأخير في مساره، ينتقل إلى حالة `FINISHED`، وتنتهي المحاكاة.

### ٤. تعليمات تشغيل البرنامج

1.  **المتطلبات:** تأكد من أن لديك Python 3 مثبت على جهازك.
2.  **حفظ الكود:** احفظ كود بايثون المقدم في ملف باسم `robot_simulation.py` (أو أي اسم آخر بامتداد `.py`).
3.  **التشغيل من الطرفية:** افتح الطرفية (terminal) أو موجه الأوامر (command prompt)، انتقل إلى المجلد الذي حفظت فيه الملف، وقم بتشغيل الأمر التالي:
    ```bash
    python robot_simulation.py
    ```
4.  **مراقبة المحاكاة:** ستبدأ المحاكاة في العمل في الطرفية. سترى الشبكة تُطبع في كل خطوة، مع الروبوت (`^`, `>`, `v`, `<`) يتحرك على طول المسار المحسوب (`*`) نحو الهدف (`G`). ستتم طباعة الحالة الحالية للروبوت أيضًا أسفل الشبكة.

