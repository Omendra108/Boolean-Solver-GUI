<h1>Boolean Expression Simplification Tool</h1>
<hr><p>This project focuses on developing a Python-based tool that accepts a Boolean expression as input, simplifies the expression, and generates its corresponding truth table.</p><h2>General Information</h2>
<hr><ul>
<li>In the VLSI industry, RTL design engineers often need to simplify complex Boolean expressions to minimize chip complexity and hardware resource usage, ultimately reducing overall cost. Manually simplifying large expressions with numerous variables can be tedious and time-consuming, highlighting the need for an efficient tool to assist in this process.</li>
</ul><ul>
<li>Boolean expressions can sometimes involve a large number of variables and complex logical operations. Manually evaluating such expressions and generating their truth tables can be time-consuming and error-prone. This project offers a tool designed to simplify Boolean expressions and automatically generate their corresponding truth tables, streamlining the evaluation process and improving efficiency.</li>
</ul><ul>
<li>This project serves as a basic prototype of tools intended for use in the VLSI industry. It can act as a foundation for electrical engineers to build upon and develop more advanced software capable of addressing a broader range of challenges faced by VLSI engineers.</li>
</ul><h2>Technologies Used</h2>
<hr><ul>
<li>Python</li>
</ul><ul>
<li>Digital electronics</li>
</ul><h2>Features</h2>
<hr><ul>
<li>Users can input Boolean expressions using a combination of the machine keyboard and a built-in virtual keypad. Variables can be typed directly using the keyboard, while logical operators are selected via the virtual keypad. Any lowercase letters entered are automatically converted to uppercase, adhering to standard Boolean notation conventions.</li>
  <img width="644" height="558" alt="Screenshot 2025-07-24 094045" src="https://github.com/user-attachments/assets/6a00126e-84d9-4cb5-9083-1adf1bf1e861" />

</ul><ul>
<li>When user clicks on Table button ✅, a truth table is generated for the input expression.</li>
  <img width="1398" height="561" alt="Screenshot 2025-07-24 094136" src="https://github.com/user-attachments/assets/5b714dce-ece9-4bb8-92a1-b7d56909b4da" />

</ul><ul>
<li>When user clicks on Simplify 🔍, the simplified SOP and POS expression is generated.</li>
  <img width="1148" height="557" alt="Screenshot 2025-07-24 094235" src="https://github.com/user-attachments/assets/fb0380aa-e47c-46a8-97d2-fd06dd77ad74" />

</ul><h2>Setup</h2>
<hr><p>To run the script we need :
Python Environment(VS code) and certain libraries(mentioned in the code).</p><h2>Project Status</h2>
<hr><p>Completed (More improvements possible in future)</p><h2>Improvements</h2>
<hr><ul>
<li>Integrate the script with web application or desktop application.</li>
</ul><ul>
<li>Generate logic gate circuit using universal gates(NAND, NOR) for assisting RTL design engineers.</li>
</ul><ul>
<li>Build a CAD tool that enables users to design digital logic circuits using standard logic gate symbols. Users can visually build gate-level circuits, which the tool will automatically convert into a corresponding netlist. It will then simplify the Boolean logic and generate the equivalent Verilog code.</li>
</ul>
