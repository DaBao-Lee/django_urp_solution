function loadCredits() {

    const btn = document.getElementsByClassName('credits')[0];
    btn.innerHTML = '加载中...';
    fetch('/credits/', {
        method: 'get',
    })
    .then(res => res.json())
    .then(data => {
        let html = `
        <h2>📈 绩点信息</h2>
        <table>
            <thead>
                <tr>
                    <th>课程名</th>
                    <th>绩点</th>
                    <th>学位绩点</th>
                    <th>加权学位绩点</th>
                </tr>
            </thead>
            <tbody>
        `;
        for (let i = 0; i < data.courseName.length; i++) {
            html += `
                <tr>
                    <td>${data.courseName[i]}</td>
                    <td>${data.courseAttr[i]}</td>
                    <td>${data.coursePoints[i]}</td>
                    <td>${data.courseGrades[i]}</td>
                </tr>
            `;
        }
        html += '</tbody></table>';
        btn.style.display = 'none';
        document.getElementById("credits-area").innerHTML = html;
    })
    .catch(err => {
        console.error('加载绩点失败:', err);
        document.getElementById("credits-area").innerHTML = '<p>⛔ 无法加载绩点数据</p>';
    });
}

function showEvalInfo(){
    const evaluate_btn = document.getElementsByClassName("evaluate-btn")[0];
    evaluate_btn.innerHTML = '正在加载数据...';
    fetch('/evaluationInfo/', {
        method: 'get',
    })
    .then(res => res.json())
    .then(data => {
        let html = `
        <h2>🎯 评估信息</h2>
        <table>
            <thead>
                <tr>
                    <th>问卷名称</th>
                    <th>被评人</th>
                    <th>评估内容</th>
                    <th>是否已评估</th>
                </tr>
            </thead>
            <tbody>
        `;
        let flag = 0;
        for (let i = 0; i < data.term.length; i++) {
            html += `
                <tr>
                    <td>${data.term[i]}</td>
                    <td>${data.courseTeacher[i]}</td>
                    <td>${data.courseName[i]}</td>
                    <td>${data.evualuation[i]}</td>
                </tr>
            `;
            if (data.evualuation[i] == "是"){
                flag++;
            }
        }
        html += '</tbody></table>';
        evaluate_btn.style.display = 'none';
        document.getElementById("evaluate-area").innerHTML = html;
        if ( !(flag == data.term.length )){ 
            const start_evaluate = document.getElementsByClassName("start_evaluate")[0];
            start_evaluate.style.display = 'block';
        }
    })
    .catch(err => {
        evaluate_btn.style.display = 'none';
        console.error('加载评估数据失败:', err);
        document.getElementById("evaluate-area").innerHTML = '<p>⛔ 评估出错或暂时不需要评估</p>';
    });
}

function startEval(){
    const status = document.getElementById("status");
    fetch('/evaluation/', {
        method: 'get',
    })
    .then(res => res.json())
    .then(data => {
       if (data.status === 'success'){
          status.innerHTML = '<p>✅ 评估完毕, 即将刷新界面...</p>';
          setTimeout(() => {
            window.location.reload();
          }, 2000);
       }
       else {
          status.innerHTML = '<p>❌ 评估失败！</p>';
       }
    })
    .catch(err => {
        evaluate_btn.style.display = 'none';
        console.error('加载评估数据失败:', err);
        document.getElementById("evaluate-area").innerHTML = '<p>⛔ 评估出错或暂时不需要评估</p>';
    });
}

function checkAdmission(){
    const studentId = document.getElementsByName("username")[0];
    const password = document.getElementsByName("password")[0];

    if (!studentId.value || !password.value) {
        showAlert("Please Fill in Your Complete Username and Key！", color="rgba(255, 0, 0, 1)");
        return;
    }

    fetch('/allowance/', {
        method: 'post',
        body: JSON.stringify({
            username: studentId.value,
            password: password.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
      .then(data => {
          if (data.status === 'success') {
              showAlert("You Get the Allowance...");
              password.value = "";
          } else {
              showAlert("You Don't Get the Allowance...", color="rgba(255, 0, 0, 1)");
          }
      });
}

function showAlert(message, color="rgba(87, 206, 82, 1)") {
    const container = document.getElementById("alert-container");
    const alertBox = document.createElement("div");

    alertBox.className = "alert alert-warning rounded fade-up";
    if (message === "You Get the Allowance..." || message === "登录成功！"){
        alertBox.innerHTML = `<i style="margin-right: 5px" class="fa fa-check-circle"></i>${message}`; // Bootstrap Icons
    } else {
        alertBox.innerHTML = `<i style="margin-right: 5px" class="fa fa-times-circle"></i>${message}`; // Bootstrap Icons
    }
    alertBox.style.background = color;
    alertBox.style.color = "#fff";
    alertBox.style.border = "none";
    alertBox.style.fontWeight = "bold";

    container.appendChild(alertBox);

    setTimeout(() => {
        container.removeChild(alertBox);
    }, 2000);
}

function scrollToSection() {
    const target = document.getElementsByClassName("target-section")[0];
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  }
