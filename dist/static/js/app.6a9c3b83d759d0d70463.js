webpackJsonp([1],{"/jgw":function(t,e,s){"use strict";function n(t){s("JnFE")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("lhb0"),i=s("SRUn"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},"08A+":function(t,e){},"0cO8":function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"app"}},[t.compute_is_main_page?s("System_Container",{attrs:{should_auto_login:t.should_create_auto_login}}):t._e(),t._v(" "),s("router-view")],1)},o=[],i={render:n,staticRenderFns:o};e.a=i},"3lqG":function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=s("EtNn"),o=s("li0J"),i=s("VU/8"),a=i(n.a,o.a,!1,null,null,null);e.default=a.exports},"7Mb/":function(t,e){},"84Lh":function(t,e,s){"use strict";var n=s("AsY6"),o=s("uflI"),i=s("dv9A");e.a={name:"Prompt",components:{Content_Element:o.default,SuggestionList:i.default,Content_Rate_Element:n.default},props:["Suggestion","Previous_Result","Prompt","Context","Body_Of_Task","Type","Is_Example","Is_Modifiable"],data:function(){return{example_prompt:"Try to rewrite the following text to be about sports",example_suggestions:[{message:"Make this text talk about soldiers"},{message:"the brother and sister could be soldiers "}],example_content:{Content:"My brother and sister fought alot ",Previous_Content:"My brother and sister Jeane got in fights all the time. One day",History:"Sample context to help impact decision",Type:"rewrite",Is_Modifiable:this.Is_Modifiable}}},computed:{compute_view_type:function(){return"Rate"==this.Type},computed_prompt:function(){return void 0===this.Prompt?this.example_prompt:this.Prompt},computed_task_type:function(){return void 0===this.Type?"_Placeholder_":this.Type},computed_suggestions:function(){return void 0===this.Suggestion?this.example_suggestions:this.Suggestion},computed_task_content:function(){return void 0===this.Content?this.example_content:this.Content}}}},"86rg":function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=s("ZFRR"),o=s("Z2bE"),i=s("VU/8"),a=i(n.a,o.a,!1,null,null,null);e.default=a.exports},"8gCy":function(t,e){},A9mU:function(t,e){},AsY6:function(t,e,s){"use strict";function n(t){s("mXmA")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("zXcd"),i=s("TZve"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},DKMl:function(t,e,s){"use strict";function n(t){s("A9mU")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("uLxJ"),i=s("oTO1"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},EtNn:function(t,e,s){"use strict";e.a={name:"Radio_Button",props:["name","label","value"],computed:{radioButtonValue:{get:function(){return this.value},set:function(){this.$emit("change",this.label)}}}}},"FWz+":function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"instruction_section"}},[s("div",{staticClass:"instruction_body"},[t._m(0),t._v(" "),s("div",{attrs:{id:"instruction"}},[s("p",{staticClass:"align_left"},[t._v(" "+t._s(t.computed_instructions)+" ")])]),t._v(" "),s("div",[t._v("Examples")]),t._v(" "),t._l(t.Supplemental,function(e){return s("div",[s("div",{domProps:{innerHTML:t._s(e)}}),t._v(" "),s("div")])})],2)])},o=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"type"}},[s("u",[t._v(" Instructions ")])])}],i={render:n,staticRenderFns:o};e.a=i},GRV1:function(t,e){},Hvnp:function(t,e){},JnFE:function(t,e){},KH91:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"container"}},[t.which_page("Login")?s("Login",{attrs:{should_auto_login:t.should_auto_login}}):t._e(),t._v(" "),t.which_page("Project")?s("Project",{attrs:{Has_Session_Expired:t.has_session_expired_function}}):t._e(),t._v(" "),t.which_page("Finished")?s("Finished",{attrs:{Tasks_Completed:t.compute_submission_count,Code:t.computed_name}}):t._e()],1)},o=[],i={render:n,staticRenderFns:o};e.a=i},LQ1U:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("div",{attrs:{id:"prev_content"}},[s("span",[s("b",[t._v(t._s(t.computed_example_text)+" Main Text To Evaluate")])]),t._v(" "),s("div",{class:t.lower_opacity_if_example(),attrs:{id:"body_of_prev_content"}},[t._v("\n        "+t._s(t.Body_Of_Task)+"\n          ")])]),t._v(" "),s("div",{attrs:{id:"compare_respond"}},[s("div",{attrs:{id:"viewable_content"}},[s("div",{attrs:{id:"suggestion_list"}},[s("SuggestionList",{attrs:{Suggestion_List:t.Suggestion_List}})],1),t._v(" "),s("div",{attrs:{id:"context"}},[""!=t.Context&&"undefined"!=t.Context?s("span",[s("b",[t._v(t._s(t.computed_example_text)+" Context")])]):t._e(),t._v("\n          "+t._s(t.Context)+"\n      ")])]),t._v(" "),s("div",{attrs:{id:"user_input"}},[s("div",[s("b",[s("u",[t._v(t._s(t.computed_example_text)+" Enter User Input Below")])])]),t._v(" "),s("textarea",{directives:[{name:"model",rawName:"v-model",value:t.user_input,expression:"user_input"}],staticClass:"text_area",domProps:{value:t.user_input},on:{input:function(e){e.target.composing||(t.user_input=e.target.value)}}})])])])},o=[],i={render:n,staticRenderFns:o};e.a=i},LqQL:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=s("qh4r"),o=s("c53c"),i=s("VU/8"),a=i(n.a,o.a,!1,null,null,null);e.default=a.exports},M93x:function(t,e,s){"use strict";var n=s("xJD8"),o=s("0cO8"),i=s("VU/8"),a=i(n.a,o.a,!1,null,null,null);e.a=a.exports},MW4G:function(t,e,s){"use strict";e.a={props:["Instructions","Supplemental"],data:function(){return{example_task_type:"Rewriting content <b>(This is an example)</b>",example_instructions:"This Is Example - You will be shown text and be asked to rewrite it the best of your ability. Make modifications as best you can. Make what changes you can, but do not overthink it. This is only meant to take a few minutes",example_supplemental:"<b>This is an EXAMPLE </b> For example, you might be asked to rewrite a few sentences from an article, but make it more suspenseful, or change the context. <p>'<b>More suspenseful</b>: The man walked to the store' -> 'The man frantically hurried to the shop'</p><p>'<b>Make about food at store</b>: I thought those pizzas at the party were disgusting' -> 'I couldn't stand the burgers at Burger King'</p>"}},computed:{computed_task_type:function(){return void 0===this.Task_Type?this.example_task_type:this.Task_Type},computed_instructions:function(){return void 0===this.Instructions?this.example_instructions:this.Instructions},computed_supplemental:function(){return void 0===this.Supplemental?this.example_supplemental:this.Supplemental}},methods:{}}},NHnr:function(t,e,s){"use strict";function n(t){if("task"in t){if("project_state"in t.task&&"Finished"==t.task.project_state)return;if("Suggestion"in t.task){var e=t.task.Suggestion;(void 0===e?"undefined":a()(e))==a()("")&&(e=""==e?[]:[e]);for(var s=0;s<e.length;s++)e[s]={message:e[s]};t.task.Suggestion=e}}}function o(t){var e={Explanation:"",Examples:[]};return"task"in t&&"instructions"in t.task&&(e=t.task.instructions),e}Object.defineProperty(e,"__esModule",{value:!0});var i=s("pFYg"),a=s.n(i),r=s("7+uW"),u=s("M93x"),_=s("YaEn");r.a.config.productionTip=!1,new r.a({el:"#app",router:_.a,template:"<App/>",components:{App:u.a},data:{stored_state:{state:{name:"",password:"",amount_of_content_submitted:0,current_project_state:"Login",current_result:"Enter Response Here",current_rating:"",current_task:{task:{Prompt:"Take a gun and end it",Suggestion:[{message:"bahhh black wfwee"}],Body_Of_Task:"fuck you",Context:"This is arbitrary",Type:"rate",instructions:[]}},current_instructions:{Explanation:"",Examples:[]},max_session_time:420,_start_time:(new Date).getTime()/1e3},setNameAndPassword:function(t,e){this.state.name=t,this.state.password=e},initialize_session_time_and_start_time:function(t){"task"in t&&"Session_Time"in t.task&&(console.log("YAY"),this.state.max_session_time=t.task.Session_Time,this.state._start_time=(new Date).getTime()/1e3)},setProjectState:function(t){"task"in t&&"Project_State"in t.task&&(this.state.current_project_state=t.task.Project_State)},setTask:function(t){n(t),this.state.current_task=t},setInstructions:function(t){this.state.current_instructions=o(t),console.log("CURRENT INSTRUCTIONS"),console.log(this.state.current_instructions)},set_result:function(t){console.log("UPDATING"+t),this.state.current_result=t},set_rating:function(t){this.state.current_rating=t},clear_user_feedback:function(){this.state.current_result="",this.state.current_rating="",console.log("THE USER INPUT HAS CHANGE IT SHOULD BE UPDATED EVERYWHERE"),console.log(this.state.current_result)},increment_submissions:function(){var t=this.state.amount_of_content_submitted;this.state.amount_of_content_submitted=t+1},has_session_expired:function(){var t=this.state._start_time;return!((new Date).getTime()/1e3-t<this.state.max_session_time)}}}})},SRUn:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("div",{attrs:{id:"page"}},[s("div",{attrs:{id:"header"}},[s("div",{staticClass:"header_element",on:{click:function(e){t.set_page("Instruction")}}},[t._m(0)]),t._v(" "),s("div",{staticClass:"header_element",on:{click:function(e){t.set_page("Task")}}},[t._m(1)])]),t._v(" "),s("div",{attrs:{id:"hint"}},[t._v("Use Example for help or Click Current_Task to return to the current task ")]),t._v(" "),s("div",{attrs:{id:"project"}},[t.which_page("Task")?s("Task",t._b({attrs:{Is_Example:t.test_example,Is_Modifiable:t.can_modify}},"Task",t.computed_task,!1)):t._e(),t._v(" "),t.which_page("Instruction")?s("Instruction",{attrs:{Instructions:t.computed_instructions,Supplemental:t.computed_instruction_examples}}):t._e(),t._v(" "),s("div",{staticClass:"pad_top"},[t.which_page("Instruction")?s("button",{on:{click:function(e){t.set_page("Task")}}},[t._v(" Click To Begin Task ")]):t._e(),t._v(" "),t.which_page("Task")?s("button",{on:{click:t.submit_response}},[t._v(" Click To Submit ")]):t._e()])],1)])])},o=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("b",[s("button",[t._v("Instruction Page")])])},function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("b",[s("button",[t._v("Current_Task")])])}],i={render:n,staticRenderFns:o};e.a=i},"Sm++":function(t,e,s){"use strict";var n=s("mvHQ"),o=s.n(n),i=s("7t+N"),a=s.n(i),r=s("uflI"),u=s("dv9A"),_=s("l98k"),c=s("/jgw"),l=s("xJsL"),d=s("LqQL"),p=s("DKMl");e.a={name:"container",components:{Content_Element:r.default,SuggestionList:u.default,Prompt:_.default,Project:c.default,Login:l.default,Finished:d.default,Show_Results:p.default},props:["should_auto_login"],data:function(){return{fake_result:"",how_are_you:"hello how are you tryfwefefewin",default_statement:"Write Text Here",items:[{message:"ffefew ffdsf"},{message:"Bfar"},{message:"Bar"}]}},created:function(){window.beforeunload=this.disconnect_user,document.beforeunload=this.disconnect_user,document.addEventListener("beforeunload",this.disconnect_user),window.onbeforeunload=this.disconnect_user,window.onblur=this.refresh_page},methods:{refresh_page:function(t){window.location.reload(!0)},which_page:function(t){return t==this.computed_project_state},has_session_expired_function:function(){return console.log("WHEN IS HTIS CHANGED"),this.$root.$data.stored_state.has_session_expired()},disconnect_user:function(t){console.log(t);var e=this.$root.$data.stored_state.state.name,s=this.$root.$data.stored_state.state.password;a.a.ajax({url:"/api/disconnect",data:"jsonData="+o()({name:e,password:s}),type:"POST",async:!1,success:function(t){var t=JSON.parse(t);console.log("WE ARE STOPPED"),window.location.reload()}.bind(this)})}},computed:{computed_task:function(){return this.$root.$data.stored_state.state.current_task},computed_project_state:function(){return this.$root.$data.stored_state.state.current_project_state},computed_name:function(){return""!=this.$root.$data.stored_state.state.name?this.$root.$data.stored_state.state.name:""},compute_submission_count:function(){return this.$root.$data.stored_state.state.amount_of_content_submitted}}}},TTDU:function(t,e,s){"use strict";var n=s("86rg"),o=s("dv9A");e.a={props:["Content","Context","Body_Of_Task","Type","Is_Example","Is_Modifiable","Suggestion_List"],components:{radio_list:n.default,SuggestionList:o.default},data:function(){return{example_text:"THIS IS AN EXAMPLE FOR REFERENCE:",example_explained:" The following text written below is an example of a user taking the content highlighted yellow on the left and rewriting it here\r\n \r\n",user_feedback:"Enter Text Here"}},methods:{lower_opacity_if_example:function(){return this.compute_is_example?"low_opacity":"high_opacity"},background_border_and_red:function(){return this.compute_is_example?["background_red","text_area"]:"text_area"}},computed:{user_input:{get:function(){return this.$root.$data.stored_state.state.current_result},set:function(t){this.$root.$data.stored_state.set_result(t)}},compute_is_modifiable:function(){return void 0!==this.Is_Modifiable&&this.Is_Modifiable},compute_is_example:function(){return void 0===this.Is_Example||this.Is_Example},computed_example_text:function(){return this.compute_is_example?this.example_text:""},computed_explain_text:function(){return this.compute_is_example?this.example_explained:""}}}},TZve:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("div",{attrs:{id:"prev_content"}},[s("span",[s("b",[t._v(t._s(t.computed_example_text)+" Original Content ")])]),t._v(" "),s("div",{class:t.lower_opacity_if_example(),attrs:{id:"body_of_prev_content"}},[t._v("\n        "+t._s(t.Body_Of_Task)+"\n          ")])]),t._v(" "),s("div",{attrs:{id:"compare_respond"}},[s("div",{attrs:{id:"viewable_content"}},[s("div",{attrs:{id:"suggestion_list"}},[s("SuggestionList",{attrs:{Suggestion_List:t.Suggestion_List}})],1),t._v(" "),s("div",{attrs:{id:"context"}},[""!=t.Context&&"undefined"!=t.Context?s("span",[s("b",[t._v(t._s(t.computed_example_text)+" Context")])]):t._e(),t._v("\n          "+t._s(t.Context)+"\n      ")])]),t._v(" "),s("div",{attrs:{id:"user_input"}},[s("div",[s("b",[s("u",[t._v(t._s(t.computed_example_text)+" Content To Be Evaluated ")])])]),t._v(" "),s("div",{class:t.background_border_and_red()},[s("p",[t._v("   "+t._s(t.Content)+" ")])]),t._v(" "),s("div",{attrs:{id:"rating"}},[t._m(0),t._v(" "),s("radio_list",{attrs:{Is_Modifiable:t.Is_Modifiable}})],1)])])])},o=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("b",[t._v(" Rate "),s("u",[t._v(" Above ")]),t._v(" On Quality Of Achieving Prompt: ")])}],i={render:n,staticRenderFns:o};e.a=i},UZHQ:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"Login_Section"}},[t._m(0),t._v(" "),s("div",[s("b",[t._v("Code: "+t._s(t.random_code))])]),t._v(" "),s("div",[s("div",[t.logged_in?t._e():s("label",{staticClass:"login"},[t._v(" Name: ")]),t._v(" "),t.logged_in?s("label",[t._v("Logged in as: "+t._s(t.name))]):s("form",[s("input",{directives:[{name:"model",rawName:"v-model",value:t.name,expression:"name"}],attrs:{type:"text",name:"name"},domProps:{value:t.name},on:{input:function(e){e.target.composing||(t.name=e.target.value)}}})])]),t._v(" "),t.logged_in?t._e():s("div",{staticClass:"login_section"},[s("label",{staticClass:"login"},[t._v("Password:")]),t._v(" "),s("form",[s("input",{directives:[{name:"model",rawName:"v-model",value:t.password,expression:"password"}],attrs:{type:"text",name:"password"},domProps:{value:t.password},on:{input:function(e){e.target.composing||(t.password=e.target.value)}}})])])]),t._v(" "),t._m(1),t._v(" "),s("div",{staticClass:"align_submit_buttons"},[t.logged_in?t._e():s("button",{on:{click:t.submit}},[t._v("login")])])])},o=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"explanation_location"}},[s("span",{staticClass:"explanation"},[t._v("Use this code for name and password (Please remember it) and click submit")])])},function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("p")])}],i={render:n,staticRenderFns:o};e.a=i},XYWp:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"Element"},[s("div",{staticClass:"Prompt_Box"},[s("h3",[t._v("Prompt:  "+t._s(t.computed_prompt)+"  ")])]),t._v(" "),t.compute_view_type?s("Content_Rate_Element",{attrs:{Content:t.Previous_Result,Body_Of_Task:t.Body_Of_Task,Type:t.Type,Context:t.Context,Is_Example:t.Is_Example,Suggestion_List:t.computed_suggestions}}):s("Content_Element",{attrs:{Body_Of_Task:t.Body_Of_Task,Type:t.Type,Context:t.Context,Is_Example:t.Is_Example,Suggestion_List:t.computed_suggestions}})],1)},o=[],i={render:n,staticRenderFns:o};e.a=i},Y972:function(t,e,s){"use strict";e.a={props:["Suggestion_List"],data:function(){return{sample_suggestions:[{message:"THIS SHOULD NOT SHOW Suggestion one to help advise your modifications"},{message:"THIS SHOULD NOT SHOW Suggestion two to help advise your modifications"}]}},computed:{computed_suggestions:function(){return void 0===this.Suggestion_List?this.sample_suggestions:this.Suggestion_List},computed_header:function(){return 0==this.computed_suggestions.length?"":"Info"}}}},YaEn:function(t,e,s){"use strict";var n=s("Dd8w"),o=s.n(n),i=s("7+uW"),a=s("/ocq"),r=[{path:"/Home",component:"Home"},{path:"/Project_Container",component:"Project_Container"},{path:"/Task",component:"Task"},{path:"/Instruction",component:"Instruction"},{path:"/Login",component:"Login"},{path:"/Finished",component:"Finished"},{path:"/Content_Element",component:"Content_Element"},{path:"/Show_Results",component:"Show_Results"},{path:"/System_Container",component:"System_Container"},{path:"/text_block",component:"text_block"}],u=r.map(function(t){return o()({},t,{component:function(){return s("mUJ2")("./"+t.component+".vue")}})});i.a.use(a.a),e.a=new a.a({routes:u,mode:"history"})},Z2bE:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("radio_button",{attrs:{name:"options",label:"Issue",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),s("radio_button",{attrs:{name:"options",label:"1",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),s("radio_button",{attrs:{name:"options",label:"2",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),s("radio_button",{attrs:{name:"options",label:"3",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),s("radio_button",{attrs:{name:"options",label:"4",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),s("radio_button",{attrs:{name:"options",label:"5",value:t.selectedValue},on:{change:t.changeValue}})],1)},o=[],i={render:n,staticRenderFns:o};e.a=i},ZFRR:function(t,e,s){"use strict";var n=s("3lqG");e.a={name:"radio_list",components:{radio_button:n.default},props:["Is_Modifiable"],data:function(){return{selectedValue:this.$root.$data.stored_state.state.result}},methods:{changeValue:function(t){this.$root.$data.stored_state.set_rating(t),this.$root.$data.stored_state.set_result(t)}}}},ZJd5:function(t,e,s){"use strict";var n=s("mvHQ"),o=s.n(n),i=s("7t+N"),a=s.n(i);e.a={name:"text_block",props:{Text:{default:"Default_Text Placed Here"},Associated_Content_ID:{default:39},Associated_Process_ID:{default:1}},data:function(){return{remove_enum:"remove",promote_enum:"promote",place_holder:this.Text}},watch:{place_holder:function(t,e){return console.log("WTF"),"777"}},methods:{send_edit:function(t,e,s,n){console.log(s),console.log(t),console.log(e),a.a.ajax({url:"/api/edit",data:"jsonData="+o()({process_id:t,content_id:e,edit_type:s,result:n}),type:"POST",success:function(t){console.log(t);var t=JSON.parse(t);t.results}.bind(this)})}},computed:{computed_text:function(){return console.log("AGRO NOW"),this.place_holder!=this.Text?this.Text:this.place_holder},compute_text_area_input_value:function(){return console.log(this.$refs.Text_Result.value),this.$refs.Text_Result.value}}}},c53c:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[t.compute_work_done?s("p",[t._v("Thank you for your time. COPY AND USE the following code before "),s("u",[t._v("leaving or switching from the current\n    page ")]),t._v(": "+t._s(t.Code)+"\n  ")]):s("p",[t._v("   Currently there are no available queries to do at this time. Please come by at another time, no code will be provided")])])},o=[],i={render:n,staticRenderFns:o};e.a=i},dv9A:function(t,e,s){"use strict";function n(t){s("wu3u")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("Y972"),i=s("dvTN"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},dvTN:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"list_alignment"},[s("ul",{staticClass:"list_element"},[s("span",[s("b",[s("i",[t._v(" "+t._s(t.computed_header))])])]),t._v(" "),t._l(t.computed_suggestions,function(e){return s("li",[t._v("\n    "+t._s(e.message)+"\n  ")])})],2)])},o=[],i={render:n,staticRenderFns:o};e.a=i},hHJz:function(t,e,s){"use strict";function n(t){s("7Mb/")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("ZJd5"),i=s("rx3X"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},hjgi:function(t,e,s){"use strict";function n(t){s("8gCy")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("Sm++"),i=s("KH91"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},kmF9:function(t,e){},l98k:function(t,e,s){"use strict";function n(t){s("Hvnp")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("84Lh"),i=s("XYWp"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},lhb0:function(t,e,s){"use strict";var n=s("mvHQ"),o=s.n(n),i=s("7t+N"),a=s.n(i),r=s("uflI"),u=s("LqQL"),_=s("l98k"),c=s("mg6j");s("xJsL");e.a={name:"Project_Container",components:{Content_Element:r.default,Task:_.default,Instruction:c.default,Finished:u.default},data:function(){return{current_page:"Instruction",last_task_type:"",can_modify:!0,test_example:!1}},props:["Has_Session_Expired"],methods:{logic:function(t){this.$root.$data.stored_state.clear_user_feedback(),this.set_page_from_server(t),this.$root.$data.stored_state.setTask(t),this.$root.$data.stored_state.setProjectState(t),this.$root.$data.stored_state.setInstructions(t),this.$root.$data.stored_state.increment_submissions()},which_page:function(t){return t==this.current_page},set_page:function(t){this.current_page=t},set_page_from_server:function(t){this.current_page="",this.current_page="Instruction"},submit_response:function(){var t=this.$root.$data.stored_state.state.name,e=this.$root.$data.stored_state.state.password,s=this.$root.$data.stored_state.state.current_result,n=this.Has_Session_Expired();a.a.ajax({url:"/api/submit",data:"jsonData="+o()({name:t,password:e,results:s,session_expired:n}),type:"POST",success:function(t){var t=JSON.parse(t);this.logic(t)}.bind(this)})}},computed:{computed_instructions:function(){return this.$root.$data.stored_state.state.current_instructions.Explanation},computed_instruction_examples:function(){return this.$root.$data.stored_state.state.current_instructions.Examples},computed_task:function(){return this.$root.$data.stored_state.state.current_task.task},computed_prompt:function(){var t=this.computed_task;return console.log(t),prompt in t.task?t.task.Prompt:null},computed_body_of_task:function(){var t=this.computed_task;return console.log(t),prompt in t.task?t.task.body_of_task:null},computed_suggestions:function(){var t=this.computed_task;return prompt in t.task?t.task.suggestions:null}}}},li0J:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("label",{staticClass:"radio"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.radioButtonValue,expression:"radioButtonValue"}],attrs:{type:"radio",name:t.name},domProps:{value:t.label,checked:t._q(t.radioButtonValue,t.label)},on:{change:function(e){t.radioButtonValue=t.label}}}),t._v(" "),s("span",[t._v(t._s(t.label))])])},o=[],i={render:n,staticRenderFns:o};e.a=i},mUJ2:function(t,e,s){function n(t){var e=o[t];return e?Promise.all(e.slice(1).map(s.e)).then(function(){return s(e[0])}):Promise.reject(new Error("Cannot find module '"+t+"'."))}var o={"./Content_Element.vue":["uflI"],"./Content_Rate_Element.vue":["AsY6"],"./Finished.vue":["LqQL"],"./Instruction.vue":["mg6j"],"./Login.vue":["xJsL"],"./Project_Container.vue":["/jgw"],"./Show_Results.vue":["DKMl"],"./SuggestionList.vue":["dv9A"],"./System_Container.vue":["hjgi"],"./Task.vue":["l98k"],"./radio_button_list/radio_button.vue":["3lqG"],"./radio_button_list/radio_list.vue":["86rg"],"./text_block.vue":["hHJz"]};n.keys=function(){return Object.keys(o)},n.id="mUJ2",t.exports=n},mXmA:function(t,e){},mg6j:function(t,e,s){"use strict";function n(t){s("08A+")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("MW4G"),i=s("FWz+"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},"nKb+":function(t,e,s){"use strict";var n=s("mvHQ"),o=s.n(n),i=s("7t+N"),a=s.n(i);e.a={name:"Login",props:{should_auto_login:{default:!1}},data:function(){return{random_code:Math.round(1e6*Math.random())+"C"+Math.round(1e7*Math.random())+"LX",logged_in:!1,password:"",name:""}},mounted:function(){window.onload=function(){console.log("GREAT stuff yee"),console.log(this.is_auto_login),console.log("wtf this should log in huh"),console.log(this.is_auto_login),1==this.is_auto_login&&(this._show_everything_but_login(),this.password=this.random_code,this.name=this.random_code,this.submit())}.bind(this)},computed:{is_auto_login:function(){return this.should_auto_login}},methods:{logic:function(t,e,s){this.$root.$data.stored_state.clear_user_feedback(),this.$root.$data.stored_state.setNameAndPassword(t,e),this.$root.$data.stored_state.setProjectState(s),this.$root.$data.stored_state.setTask(s),this.$root.$data.stored_state.setInstructions(s),this.$root.$data.stored_state.initialize_session_time_and_start_time(s)},logout:function(){this.$data.logged_in=!1},register_account:function(){},_show_only_login:function(){var t=a.a.noConflict();t("#app").css({visibility:"hidden",display:"block"}),t("#Login_Section").css({visibility:"visible",display:"block"})},_show_everything_but_login:function(){var t=a.a.noConflict();t("#app").css({visibility:"visible",display:"block"}),t("#Login_Section").css({visibility:"hidden",display:"none"})},submit:function(t){return""==this.name||"Invalid Name"==this.name?void(this.name="Invalid Name"):""==this.password||"Invalid Password"==this.password||""==this.password?void(this.password="Invalid Password"):void a.a.ajax({url:"/api/login",data:"jsonData="+o()({name:this.name,password:this.password}),type:"POST",success:function(t){var t=JSON.parse(t);console.log("login request"),console.log(t),"failure"==t.task?(this.name="Wrong Code",this.password="Wrong Code",this.logged_in=!1):this.logic(this.name,this.password,t)}.bind(this)})}}}},oTO1:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"flex_box_row ui container"},[s("div",{staticClass:"ui pointing menu add_wrap"},t._l(t.all_processes,function(e){return s("span",[s("a",{staticClass:"item",on:{click:function(s){t.get_results(e.process_id)}}},[e.is_locked?s("i",{staticClass:"green check icon"}):e.in_progress?s("i",{staticClass:"yellow circle check outline icon"}):e.is_ready?s("i",{staticClass:"yellow  circle outline icon"}):0==e.is_ready?s("i",{staticClass:"red minus square outline icon"}):t._e(),t._v("\n\n\n          "+t._s(e.process_id))])])})),t._v(" "),s("div",{staticClass:"ui segment"},[s("div",{attrs:{id:"prompt "},on:{click:function(e){t.get_results()}}},[s("h3",[t._v("Prompt ")]),t._v(t._s(t.prompt)+" ")]),t._v(" "),s("div",{attrs:{id:"body"}},[s("p",[t._v(t._s(t.body)+" ")])]),t._v(" "),s("div",{attrs:{id:"result"}},[s("b",[t._v(t._s(t.result)+" ")])]),t._v(" "),s("div",{attrs:{id:"user_inputs"}},t._l(t.content,function(e){return s("div",[s("text_block",{attrs:{Text:e[1],Associated_Content_ID:e[0],Associated_Process_ID:t.process_id}}),t._v(" "),t._m(0,!0)],1)}))])])},o=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("p",[s("i")])}],i={render:n,staticRenderFns:o};e.a=i},qh4r:function(t,e,s){"use strict";e.a={name:"Finished",props:{Tasks_Completed:{default:0,type:Number},Code:{default:"-1"}},computed:{compute_work_done:function(){return this.Tasks_Completed>0}}}},rx3X:function(t,e,s){"use strict";var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"ui segment"},[t._m(0),t._v(" "),s("div",[s("div",[s("textarea",{ref:"Text_Result",staticClass:"ui segment focus input_box",attrs:{id:"Text_Result"},domProps:{value:t.computed_text}})]),t._v(" "),s("div",{staticClass:"ui segment"},[s("br"),t._v("content_id "+t._s(t.Associated_Content_ID)+"  process_id "+t._s(t.Associated_Process_ID)+"\n\n    ")]),t._v(" "),s("div",{staticClass:"ui divider"}),t._v(" "),s("div",{staticClass:"ui primary button",on:{click:function(e){t.send_edit(t.Associated_Process_ID,t.Associated_Content_ID,t.promote_enum,t.compute_text_area_input_value)}}},[t._v("Keep")]),t._v(" "),s("div",{staticClass:"ui button",on:{click:function(e){t.send_edit(t.Associated_Process_ID,t.Associated_Content_ID,t.remove_enum,t.compute_text_area_input_value)}}},[t._v("Negate")])])])},o=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"ui top attached label"},[s("a",{staticClass:"item"},[t._v("\n    Result\n  ")])])}],i={render:n,staticRenderFns:o};e.a=i},uLxJ:function(t,e,s){"use strict";var n,o=s("bOdI"),i=s.n(o),a=s("mvHQ"),r=s.n(a),u=s("7t+N"),_=s.n(u),c=(s("hHJz"),s("hHJz"));e.a=(n={components:{Text_block:c.default},name:"Show_Results",data:function(){return{all_processes:[],prompt:"",result:"",body:"",is_finished:!1,process_id:-1,content:[]}},mounted:function(){this.get_results()},methods:{map_state:function(t){this.prompt=t.prompt,this.result=t.result,this.body=t.body,this.is_finished=t.is_finished,this.process_id=t.process_id,this.all_processes=t.processes_state,this.content=t.content},copy_value:function(t){return console.log(t),console.log("WTF"),t},get_results:function(t){var t=t;_.a.ajax({url:"/api/get_results",data:"jsonData="+r()({id:t}),type:"POST",success:function(t){console.log(t);var t=JSON.parse(t),e=t.results;this.map_state(e)}.bind(this)})}}},i()(n,"mounted",function(){this.get_results(-1)}),i()(n,"computed",{}),n)},uflI:function(t,e,s){"use strict";function n(t){s("GRV1")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("TTDU"),i=s("LQ1U"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},wu3u:function(t,e){},xJD8:function(t,e,s){"use strict";var n=s("7t+N"),o=(s.n(n),s("uflI"),s("dv9A"),s("l98k"),s("/jgw"),s("xJsL"),s("LqQL"),s("DKMl"),s("hHJz"),s("hjgi"));e.a={name:"app",components:{System_Container:o.default},data:function(){return{should_create_auto_login:!0}},mounted:function(){this.compute_is_main_page},computed:{compute_is_main_page:function(){var t=window.location.href.split("/");return""==t[t.length-1]}}}},xJsL:function(t,e,s){"use strict";function n(t){s("kmF9")}Object.defineProperty(e,"__esModule",{value:!0});var o=s("nKb+"),i=s("UZHQ"),a=s("VU/8"),r=n,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},zXcd:function(t,e,s){"use strict";var n=s("86rg"),o=s("dv9A");e.a={props:["Content","Context","Body_Of_Task","Type","Is_Example","Is_Modifiable","Suggestion_List"],components:{radio_list:n.default,SuggestionList:o.default},data:function(){return{example_text:"THIS IS AN EXAMPLE FOR REFERENCE:",example_explained:" The following text written below is an example of a user taking the content highlighted yellow on the left and rewriting it here\r\n \r\n",user_feedback:"Enter Text Here"}},methods:{lower_opacity_if_example:function(){return this.compute_is_example?"low_opacity":"high_opacity"},background_border_and_red:function(){return["background_red","text_area"]}},computed:{user_input:{get:function(){return this.compute_is_modifiable?this.$root.$data.stored_state.state.current_result:""},set:function(t){this.compute_is_modifiable&&this.$root.$data.stored_state.set_result(t)}},compute_is_modifiable:function(){return void 0!==this.Is_Modifiable&&this.Is_Modifiable},compute_is_example:function(){return void 0===this.Is_Example||this.Is_Example},computed_example_text:function(){return this.compute_is_example?this.example_text:""},computed_explain_text:function(){return this.compute_is_example?this.example_explained:""}}}}},["NHnr"]);
//# sourceMappingURL=app.6a9c3b83d759d0d70463.js.map