webpackJsonp([7],{"/jgw":function(t,e,n){"use strict";function s(t){n("XfsB")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("lhb0"),i=n("1Q1R"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},"08A+":function(t,e){},"1Q1R":function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{attrs:{id:"page"}},[n("div",{attrs:{id:"header"}},[n("div",{staticClass:"header_element",on:{click:function(e){t.set_page("Instruction")}}},[t._m(0)]),t._v(" "),n("div",{staticClass:"header_element",on:{click:function(e){t.set_page("Task")}}},[t._m(1)])]),t._v(" "),n("div",{attrs:{id:"hint"}},[t._v("Use Example for help or Click Current_Task to return to the current task ")]),t._v(" "),n("div",{attrs:{id:"project"}},[t.which_page("Task")?n("Task",t._b({attrs:{Is_Example:t.test_example,Is_Modifiable:t.can_modify}},"Task",t.computed_task,!1)):t._e(),t._v(" "),t.which_page("Instruction")?n("Instruction",{attrs:{Instructions:t.computed_instructions,Supplemental:t.computed_instruction_examples}}):t._e(),t._v(" "),n("div",{staticClass:"pad_top"},[t.which_page("Instruction")?n("button",{on:{click:function(e){t.set_page("Task")}}},[t._v(" Click To Begin Task ")]):t._e(),t._v(" "),t.which_page("Task")?n("button",{on:{click:t.submit_response}},[t._v(" Click To Submit ")]):t._e()])],1)])])},o=[function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b",[n("button",[t._v("Instruction Page")])])},function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b",[n("button",[t._v("Current_Task")])])}],i={render:s,staticRenderFns:o};e.a=i},"3lqG":function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s=n("EtNn"),o=n("li0J"),i=n("VU/8"),a=i(s.a,o.a,!1,null,null,null);e.default=a.exports},"5aP1":function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"ui segment"},[t._m(0),t._v(" "),n("div",[n("div",[n("textarea",{ref:"Text_Result",staticClass:"ui segment focus input_box",attrs:{id:"Text_Result"},domProps:{value:t.computed_text}})]),t._v(" "),n("div",{staticClass:"ui segment"},[n("br"),t._v("content_id "+t._s(t.Associated_Content_ID)+"  process_id "+t._s(t.Associated_Process_ID)+" score "+t._s(t.Associated_Score)+"\n        "),n("br"),t._v(" user "+t._s(t.Associated_User_ID)+"\n\n    ")]),t._v(" "),n("div",{staticClass:"ui divider"}),t._v(" "),n("div",{staticClass:"ui primary button",on:{click:function(e){t.send_edit(t.Associated_Process_ID,t.Associated_Content_ID,t.promote_enum,t.compute_text_area_input_value)}}},[t._v("Keep")]),t._v(" "),n("div",{staticClass:"ui button",on:{click:function(e){t.send_edit(t.Associated_Process_ID,t.Associated_Content_ID,t.remove_enum,t.compute_text_area_input_value)}}},[t._v("Negate")])])])},o=[function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"ui top attached label"},[n("a",{staticClass:"item"},[t._v("\n    Result\n  ")])])}],i={render:s,staticRenderFns:o};e.a=i},"84Lh":function(t,e,n){"use strict";var s=n("AsY6"),o=n("uflI"),i=n("dv9A");e.a={name:"Prompt",components:{Content_Element:o.default,SuggestionList:i.default,Content_Rate_Element:s.default},props:["Suggestion","Previous_Result","Prompt","Context","Body_Of_Task","Type","Is_Example","Is_Modifiable"],data:function(){return{example_prompt:"Try to rewrite the following text to be about sports",example_suggestions:[{message:"Make this text talk about soldiers"},{message:"the brother and sister could be soldiers "}],example_content:{Content:"My brother and sister fought alot ",Previous_Content:"My brother and sister Jeane got in fights all the time. One day",History:"Sample context to help impact decision",Type:"rewrite",Is_Modifiable:this.Is_Modifiable}}},computed:{compute_view_type:function(){return"Rate"==this.Type},computed_prompt:function(){return void 0===this.Prompt?this.example_prompt:this.Prompt},computed_task_type:function(){return void 0===this.Type?"_Placeholder_":this.Type},computed_suggestions:function(){return void 0===this.Suggestion?this.example_suggestions:this.Suggestion},computed_task_content:function(){return void 0===this.Content?this.example_content:this.Content}}}},"86rg":function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s=n("ZFRR"),o=n("Z2bE"),i=n("VU/8"),a=i(s.a,o.a,!1,null,null,null);e.default=a.exports},AsY6:function(t,e,n){"use strict";function s(t){n("mXmA")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("zXcd"),i=n("TZve"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},BWkt:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"Login_Section"}},[t._m(0),t._v(" "),n("div"),t._v(" "),n("div",[n("div",[t.logged_in?t._e():n("label",{staticClass:"login"},[t._v(" WorkedID: ")]),t._v(" "),t.logged_in?t._e():n("form",[n("input",{directives:[{name:"model",rawName:"v-model",value:t.name,expression:"name"}],attrs:{type:"text",name:"name"},domProps:{value:t.name},on:{input:function(e){e.target.composing||(t.name=e.target.value)}}})])])]),t._v(" "),t._m(1),t._v(" "),n("div",{staticClass:"align_submit_buttons"},[t.logged_in?t._e():n("button",{on:{click:t.submit}},[t._v("Submit")])])])},o=[function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"explanation_location"}},[n("span",{staticClass:"explanation"},[t._v("Enter your Mturk workerID,\n        "),n("br"),t._v(" If you do not, a proper completion token cannot be guaranteed\n\n    ")])])},function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("p")])}],i={render:s,staticRenderFns:o};e.a=i},DKMl:function(t,e,n){"use strict";function s(t){n("OASs")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("uLxJ"),i=n("j3HJ"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},EtNn:function(t,e,n){"use strict";e.a={name:"Radio_Button",props:["name","label","value"],computed:{radioButtonValue:{get:function(){return this.value},set:function(){this.$emit("change",this.label)}}}}},"FWz+":function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"instruction_section"}},[n("div",{staticClass:"instruction_body"},[t._m(0),t._v(" "),n("div",{attrs:{id:"instruction"}},[n("p",{staticClass:"align_left"},[t._v(" "+t._s(t.computed_instructions)+" ")])]),t._v(" "),n("div",[t._v("Examples")]),t._v(" "),t._l(t.Supplemental,function(e){return n("div",[n("div",{domProps:{innerHTML:t._s(e)}}),t._v(" "),n("div")])})],2)])},o=[function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"type"}},[n("u",[t._v(" Instructions ")])])}],i={render:s,staticRenderFns:o};e.a=i},GRV1:function(t,e){},Hvnp:function(t,e){},LQ1U:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{attrs:{id:"prev_content"}},[n("span",[n("b",[t._v(t._s(t.computed_example_text)+" Main Text To Evaluate")])]),t._v(" "),n("div",{class:t.lower_opacity_if_example(),attrs:{id:"body_of_prev_content"}},[t._v("\n        "+t._s(t.Body_Of_Task)+"\n          ")])]),t._v(" "),n("div",{attrs:{id:"compare_respond"}},[n("div",{attrs:{id:"viewable_content"}},[n("div",{attrs:{id:"suggestion_list"}},[n("SuggestionList",{attrs:{Suggestion_List:t.Suggestion_List}})],1),t._v(" "),n("div",{attrs:{id:"context"}},[""!=t.Context&&"undefined"!=t.Context?n("span",[n("b",[t._v(t._s(t.computed_example_text)+" Context")])]):t._e(),t._v("\n          "+t._s(t.Context)+"\n      ")])]),t._v(" "),n("div",{attrs:{id:"user_input"}},[n("div",[n("b",[n("u",[t._v(t._s(t.computed_example_text)+" Enter User Input Below")])])]),t._v(" "),n("textarea",{directives:[{name:"model",rawName:"v-model",value:t.user_input,expression:"user_input"}],staticClass:"text_area",domProps:{value:t.user_input},on:{input:function(e){e.target.composing||(t.user_input=e.target.value)}}})])])])},o=[],i={render:s,staticRenderFns:o};e.a=i},LqQL:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s=n("qh4r"),o=n("c53c"),i=n("VU/8"),a=i(s.a,o.a,!1,null,null,null);e.default=a.exports},M93x:function(t,e,n){"use strict";var s=n("xJD8"),o=n("v3TN"),i=n("VU/8"),a=i(s.a,o.a,!1,null,null,null);e.a=a.exports},MW4G:function(t,e,n){"use strict";e.a={props:["Instructions","Supplemental"],data:function(){return{example_task_type:"Rewriting content <b>(This is an example)</b>",example_instructions:"This Is Example - You will be shown text and be asked to rewrite it the best of your ability. Make modifications as best you can. Make what changes you can, but do not overthink it. This is only meant to take a few minutes",example_supplemental:"<b>This is an EXAMPLE </b> For example, you might be asked to rewrite a few sentences from an article, but make it more suspenseful, or change the context. <p>'<b>More suspenseful</b>: The man walked to the store' -> 'The man frantically hurried to the shop'</p><p>'<b>Make about food at store</b>: I thought those pizzas at the party were disgusting' -> 'I couldn't stand the burgers at Burger King'</p>"}},computed:{computed_task_type:function(){return void 0===this.Task_Type?this.example_task_type:this.Task_Type},computed_instructions:function(){return void 0===this.Instructions?this.example_instructions:this.Instructions},computed_supplemental:function(){return void 0===this.Supplemental?this.example_supplemental:this.Supplemental}},methods:{}}},NHnr:function(t,e,n){"use strict";function s(t){if("task"in t){if("project_state"in t.task&&"Finished"==t.task.project_state)return;if("Suggestion"in t.task){var e=t.task.Suggestion;(void 0===e?"undefined":r()(e))==r()("")&&(e=""==e?[]:[e]);for(var n=0;n<e.length;n++)e[n]={message:e[n]};t.task.Suggestion=e}}}function o(t){var e={Explanation:"",Examples:[]};return"task"in t&&"instructions"in t.task&&(e=t.task.instructions),e}function i(t){return t.replace(/[^\x00-\x7F]/g,"")}Object.defineProperty(e,"__esModule",{value:!0});var a=n("pFYg"),r=n.n(a),u=n("7+uW"),_=n("M93x"),c=n("YaEn");u.a.config.productionTip=!1,new u.a({el:"#app",router:c.a,template:"<App/>",components:{App:_.a},data:{stored_state:{state:{name:"",password:"",amount_of_content_submitted:0,current_project_state:"Login",current_result:"Enter Response Here",current_rating:"",current_task:{task:{Prompt:"Take a gun and end it",Suggestion:[{message:"bahhh black wfwee"}],Body_Of_Task:"fuck you",Context:"This is arbitrary",Type:"rate",instructions:[]}},current_instructions:{Explanation:"",Examples:[]},max_session_time:420,_start_time:(new Date).getTime()/1e3},setNameAndPassword:function(t,e){this.state.name=t,this.state.password=e},initialize_session_time_and_start_time:function(t){"task"in t&&"Session_Time"in t.task&&(console.log("YAY"),this.state.max_session_time=t.task.Session_Time,this.state._start_time=(new Date).getTime()/1e3)},setProjectState:function(t){"task"in t&&"Project_State"in t.task&&(this.state.current_project_state=t.task.Project_State)},setTask:function(t){s(t),this.state.current_task=t},setInstructions:function(t){this.state.current_instructions=o(t),console.log("CURRENT INSTRUCTIONS"),console.log(this.state.current_instructions)},set_result:function(t){t=i(t),console.log("UPDATING"+t),this.state.current_result=t},set_rating:function(t){this.state.current_rating=t},clear_user_feedback:function(){this.state.current_result="",this.state.current_rating="",console.log("THE USER INPUT HAS CHANGE IT SHOULD BE UPDATED EVERYWHERE"),console.log(this.state.current_result)},increment_submissions:function(){var t=this.state.amount_of_content_submitted;this.state.amount_of_content_submitted=t+1},has_session_expired:function(){var t=this.state._start_time;return!((new Date).getTime()/1e3-t<this.state.max_session_time)}}}})},OASs:function(t,e){},QtPA:function(t,e){},S0Jm:function(t,e){},"Sm++":function(t,e,n){"use strict";var s=n("mvHQ"),o=n.n(s),i=n("7t+N"),a=n.n(i),r=n("uflI"),u=n("dv9A"),_=n("l98k"),c=n("/jgw"),l=n("xJsL"),d=n("LqQL"),p=n("DKMl");e.a={name:"container",components:{Content_Element:r.default,SuggestionList:u.default,Prompt:_.default,Project:c.default,Login:l.default,Finished:d.default,Show_Results:p.default},props:["should_auto_login"],data:function(){return{fake_result:"",how_are_you:"hello how are you tryfwefefewin",default_statement:"Write Text Here",items:[{message:"ffefew ffdsf"},{message:"Bfar"},{message:"Bar"}]}},created:function(){window.beforeunload=this.disconnect_user,document.beforeunload=this.disconnect_user,document.addEventListener("beforeunload",this.disconnect_user),window.onbeforeunload=this.disconnect_user},methods:{refresh_page:function(t){window.location.reload(!0)},which_page:function(t){return t==this.computed_project_state},has_session_expired_function:function(){return console.log("WHEN IS HTIS CHANGED"),this.$root.$data.stored_state.has_session_expired()},disconnect_user:function(t){console.log(t);var e=this.$root.$data.stored_state.state.name,n=this.$root.$data.stored_state.state.password;a.a.ajax({url:"/api/disconnect",data:"jsonData="+o()({name:e,password:n}),type:"POST",async:!1,success:function(t){var t=JSON.parse(t);console.log("WE ARE STOPPED"),window.location.reload()}.bind(this)})}},computed:{computed_task:function(){return this.$root.$data.stored_state.state.current_task},computed_project_state:function(){return this.$root.$data.stored_state.state.current_project_state},computed_name:function(){if(""!=this.$root.$data.stored_state.state.name){var t=parseInt(100*Math.random()),e=parseInt(100*Math.random()),n=(100-t)*(100-e),s="";s=t>50?"X"+t+"Y"+e+"Z"+n:"A"+t+"B"+e+"C"+n;return this.$root.$data.stored_state.state.name+"_"+s}return""},compute_submission_count:function(){return this.$root.$data.stored_state.state.amount_of_content_submitted}}}},TTDU:function(t,e,n){"use strict";var s=n("86rg"),o=n("dv9A");e.a={props:["Content","Context","Body_Of_Task","Type","Is_Example","Is_Modifiable","Suggestion_List"],components:{radio_list:s.default,SuggestionList:o.default},data:function(){return{example_text:"THIS IS AN EXAMPLE FOR REFERENCE:",example_explained:" The following text written below is an example of a user taking the content highlighted yellow on the left and rewriting it here\r\n \r\n",user_feedback:"Enter Text Here"}},methods:{lower_opacity_if_example:function(){return this.compute_is_example?"low_opacity":"high_opacity"},background_border_and_red:function(){return this.compute_is_example?["background_red","text_area"]:"text_area"}},computed:{user_input:{get:function(){return this.$root.$data.stored_state.state.current_result},set:function(t){this.$root.$data.stored_state.set_result(t)}},compute_is_modifiable:function(){return void 0!==this.Is_Modifiable&&this.Is_Modifiable},compute_is_example:function(){return void 0===this.Is_Example||this.Is_Example},computed_example_text:function(){return this.compute_is_example?this.example_text:""},computed_explain_text:function(){return this.compute_is_example?this.example_explained:""}}}},TZve:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{attrs:{id:"prev_content"}},[n("span",[n("b",[t._v(t._s(t.computed_example_text)+" Original Content ")])]),t._v(" "),n("div",{class:t.lower_opacity_if_example(),attrs:{id:"body_of_prev_content"}},[t._v("\n        "+t._s(t.Body_Of_Task)+"\n          ")])]),t._v(" "),n("div",{attrs:{id:"compare_respond"}},[n("div",{attrs:{id:"viewable_content"}},[n("div",{attrs:{id:"suggestion_list"}},[n("SuggestionList",{attrs:{Suggestion_List:t.Suggestion_List}})],1),t._v(" "),n("div",{attrs:{id:"context"}},[""!=t.Context&&"undefined"!=t.Context?n("span",[n("b",[t._v(t._s(t.computed_example_text)+" Context")])]):t._e(),t._v("\n          "+t._s(t.Context)+"\n      ")])]),t._v(" "),n("div",{attrs:{id:"user_input"}},[n("div",[n("b",[n("u",[t._v(t._s(t.computed_example_text)+" Content To Be Evaluated ")])])]),t._v(" "),n("div",{class:t.background_border_and_red()},[n("p",[t._v("   "+t._s(t.Content)+" ")])]),t._v(" "),n("div",{attrs:{id:"rating"}},[t._m(0),t._v(" "),n("radio_list",{attrs:{Is_Modifiable:t.Is_Modifiable}})],1)])])])},o=[function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b",[t._v(" Rate "),n("u",[t._v(" Above ")]),t._v(" On Quality Of Achieving Prompt: ")])}],i={render:s,staticRenderFns:o};e.a=i},XYWp:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"Element"},[n("div",{staticClass:"Prompt_Box"},[n("h3",[t._v("Prompt:  "+t._s(t.computed_prompt)+"  ")])]),t._v(" "),t.compute_view_type?n("Content_Rate_Element",{attrs:{Content:t.Previous_Result,Body_Of_Task:t.Body_Of_Task,Type:t.Type,Context:t.Context,Is_Example:t.Is_Example,Suggestion_List:t.computed_suggestions}}):n("Content_Element",{attrs:{Body_Of_Task:t.Body_Of_Task,Type:t.Type,Context:t.Context,Is_Example:t.Is_Example,Suggestion_List:t.computed_suggestions}})],1)},o=[],i={render:s,staticRenderFns:o};e.a=i},XfsB:function(t,e){},Y972:function(t,e,n){"use strict";e.a={props:["Suggestion_List"],data:function(){return{sample_suggestions:[{message:"THIS SHOULD NOT SHOW Suggestion one to help advise your modifications"},{message:"THIS SHOULD NOT SHOW Suggestion two to help advise your modifications"}]}},computed:{computed_suggestions:function(){return void 0===this.Suggestion_List?this.sample_suggestions:this.Suggestion_List},computed_header:function(){return 0==this.computed_suggestions.length?"":"Info"}}}},YaEn:function(t,e,n){"use strict";var s=n("Dd8w"),o=n.n(s),i=n("7+uW"),a=n("/ocq"),r=[{path:"/Home",component:"Home"},{path:"/Project_Container",component:"Project_Container"},{path:"/Task",component:"Task"},{path:"/Instruction",component:"Instruction"},{path:"/Login",component:"Login"},{path:"/Finished",component:"Finished"},{path:"/Content_Element",component:"Content_Element"},{path:"/Show_Results",component:"Show_Results"},{path:"/System_Container",component:"System_Container"},{path:"/text_block",component:"text_block"},{path:"/A_Place_For_Testing",component:"A_Place_For_Testing"}],u=r.map(function(t){return o()({},t,{component:function(){return n("mUJ2")("./"+t.component+".vue")}})});i.a.use(a.a),e.a=new a.a({routes:u,mode:"history"})},Z2bE:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("radio_button",{attrs:{name:"options",label:"Issue",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),n("radio_button",{attrs:{name:"options",label:"1",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),n("radio_button",{attrs:{name:"options",label:"2",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),n("radio_button",{attrs:{name:"options",label:"3",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),n("radio_button",{attrs:{name:"options",label:"4",value:t.selectedValue},on:{change:t.changeValue}}),t._v(" "),n("radio_button",{attrs:{name:"options",label:"5",value:t.selectedValue},on:{change:t.changeValue}})],1)},o=[],i={render:s,staticRenderFns:o};e.a=i},ZFRR:function(t,e,n){"use strict";var s=n("3lqG");e.a={name:"radio_list",components:{radio_button:s.default},props:["Is_Modifiable"],data:function(){return{selectedValue:this.$root.$data.stored_state.state.result}},methods:{changeValue:function(t){this.$root.$data.stored_state.set_rating(t),this.$root.$data.stored_state.set_result(t)}}}},ZJd5:function(t,e,n){"use strict";var s=n("mvHQ"),o=n.n(s),i=n("7t+N"),a=n.n(i);e.a={name:"text_block",props:{Text:{default:"Default_Text Placed Here"},Associated_User_ID:{default:"NA"},Associated_Score:{default:-1},Associated_Content_ID:{default:39},Associated_Process_ID:{default:1}},data:function(){return{remove_enum:"remove",promote_enum:"promote",place_holder:this.Text}},watch:{place_holder:function(t,e){return console.log("WTF"),"777"}},methods:{send_edit:function(t,e,n,s){console.log(n),console.log(t),console.log(e),a.a.ajax({url:"/api/edit",data:"jsonData="+o()({process_id:t,content_id:e,edit_type:n,result:s}),type:"POST",success:function(t){console.log(t);var t=JSON.parse(t);t.results}.bind(this)})}},computed:{computed_text:function(){return console.log("AGRO NOW"),this.place_holder!=this.Text?this.Text:this.place_holder},compute_text_area_input_value:function(){return this.Text,console.log(this.$refs.Text_Result.value),this.$refs.Text_Result.value}}}},b9Z3:function(t,e){},c53c:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[t.compute_work_done?n("p",[t._v("Thank you for your time. COPY AND USE the following code before "),n("u",[t._v("leaving or switching from the current\n    page ")]),t._v(": "+t._s(t.Code)+"\n  ")]):n("p",[t._v("   Currently there are no available queries to do at this time. Please come by at another time, no code will be provided")])])},o=[],i={render:s,staticRenderFns:o};e.a=i},cQpN:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"container"}},[t.which_page("Login")?n("Login",{attrs:{should_auto_login:t.should_auto_login}}):t._e(),t._v(" "),t.which_page("Project")?n("Project",{attrs:{Has_Session_Expired:t.has_session_expired_function}}):t._e(),t._v(" "),t.which_page("Finished")?n("Finished",{attrs:{Tasks_Completed:t.compute_submission_count,Code:t.computed_name}}):t._e()],1)},o=[],i={render:s,staticRenderFns:o};e.a=i},dv9A:function(t,e,n){"use strict";function s(t){n("wu3u")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("Y972"),i=n("dvTN"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},dvTN:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"list_alignment"},[n("ul",{staticClass:"list_element"},[n("span",[n("b",[n("i",[t._v(" "+t._s(t.computed_header))])])]),t._v(" "),t._l(t.computed_suggestions,function(e){return n("li",[t._v("\n    "+t._s(e.message)+"\n  ")])})],2)])},o=[],i={render:s,staticRenderFns:o};e.a=i},hHJz:function(t,e,n){"use strict";function s(t){n("S0Jm")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("ZJd5"),i=n("5aP1"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},hjgi:function(t,e,n){"use strict";function s(t){n("b9Z3")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("Sm++"),i=n("cQpN"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},j3HJ:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"flex_box_row ui container"},[n("div",{staticClass:"ui pointing menu add_wrap"},t._l(t.all_processes,function(e){return n("span",[n("a",{staticClass:"item",on:{click:function(n){t.get_results(e.process_id)}}},[e.is_finished?n("i",{staticClass:"green check icon"}):e.in_progress?n("i",{staticClass:"yellow circle check outline icon"}):e.is_ready?n("i",{staticClass:"yellow  circle outline icon"}):0==e.is_ready?n("i",{staticClass:"red minus square outline icon"}):t._e(),t._v("\n\n\n          "+t._s(e.process_id))])])})),t._v(" "),n("div",{staticClass:"ui segment"},[n("div",{attrs:{id:"prompt "},on:{click:function(e){t.get_results()}}},[n("h3",[t._v("Prompt ")]),t._v(t._s(t.prompt)+" ")]),t._v(" "),n("div",{attrs:{id:"body"}},[n("p",[t._v(t._s(t.body)+" ")])]),t._v(" "),n("div",{attrs:{id:"result"}},[n("b",[t._v(t._s(t.result)+" ")])]),t._v(" "),n("div",{staticClass:"add_wrap",attrs:{id:"user_inputs"}},t._l(t.content,function(e){return n("div",[n("text_block",{attrs:{Text:e[1],Associated_Content_ID:e[0],Associated_User_ID:e[2],Associated_Score:e[3],Associated_Process_ID:t.process_id}}),t._v(" "),t._m(0,!0)],1)}))])])},o=[function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("p",[n("i")])}],i={render:s,staticRenderFns:o};e.a=i},l98k:function(t,e,n){"use strict";function s(t){n("Hvnp")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("84Lh"),i=n("XYWp"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},lhb0:function(t,e,n){"use strict";var s=n("mvHQ"),o=n.n(s),i=n("7t+N"),a=n.n(i),r=n("uflI"),u=n("LqQL"),_=n("l98k"),c=n("mg6j");n("xJsL");e.a={name:"Project_Container",components:{Content_Element:r.default,Task:_.default,Instruction:c.default,Finished:u.default},data:function(){return{current_page:"Instruction",last_task_type:"",can_modify:!0,test_example:!1}},props:["Has_Session_Expired"],methods:{logic:function(t){this.$root.$data.stored_state.clear_user_feedback(),this.set_page_from_server(t),this.$root.$data.stored_state.setTask(t),this.$root.$data.stored_state.setProjectState(t),this.$root.$data.stored_state.setInstructions(t),this.$root.$data.stored_state.increment_submissions()},which_page:function(t){return t==this.current_page},set_page:function(t){this.current_page=t},set_page_from_server:function(t){this.current_page="",this.current_page="Instruction"},submit_response:function(){var t=this.$root.$data.stored_state.state.name,e=this.$root.$data.stored_state.state.password,n=this.$root.$data.stored_state.state.current_result,s=this.Has_Session_Expired();a.a.ajax({url:"/api/submit",data:"jsonData="+o()({name:t,password:e,results:n,session_expired:s}),type:"POST",success:function(t){var t=JSON.parse(t);this.logic(t)}.bind(this)})}},computed:{computed_instructions:function(){return this.$root.$data.stored_state.state.current_instructions.Explanation},computed_instruction_examples:function(){return this.$root.$data.stored_state.state.current_instructions.Examples},computed_task:function(){return this.$root.$data.stored_state.state.current_task.task},computed_prompt:function(){var t=this.computed_task;return console.log(t),prompt in t.task?t.task.Prompt:null},computed_body_of_task:function(){var t=this.computed_task;return console.log(t),prompt in t.task?t.task.body_of_task:null},computed_suggestions:function(){var t=this.computed_task;return prompt in t.task?t.task.suggestions:null}}}},li0J:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("label",{staticClass:"radio"},[n("input",{directives:[{name:"model",rawName:"v-model",value:t.radioButtonValue,expression:"radioButtonValue"}],attrs:{type:"radio",name:t.name},domProps:{value:t.label,checked:t._q(t.radioButtonValue,t.label)},on:{change:function(e){t.radioButtonValue=t.label}}}),t._v(" "),n("span",[t._v(t._s(t.label))])])},o=[],i={render:s,staticRenderFns:o};e.a=i},mUJ2:function(t,e,n){function s(t){var e=o[t];return e?Promise.all(e.slice(1).map(n.e)).then(function(){return n(e[0])}):Promise.reject(new Error("Cannot find module '"+t+"'."))}var o={"./A_Place_For_Testing.vue":["C8Qq",0],"./Content_Element.vue":["uflI"],"./Content_Rate_Element.vue":["AsY6"],"./Finished.vue":["LqQL"],"./Instruction.vue":["mg6j"],"./Login.vue":["xJsL"],"./Project_Container.vue":["/jgw"],"./Show_Results.vue":["DKMl"],"./SuggestionList.vue":["dv9A"],"./System_Container.vue":["hjgi"],"./Task.vue":["l98k"],"./container_content_redux_folder/Content_Element_Redux.vue":["dJu9",2],"./container_content_redux_folder/Content_Element_Redux_Input_Type.vue":["sUbl",1],"./container_content_redux_folder/container_redux_elements/Div_Block.vue":["eBe6",5],"./container_content_redux_folder/container_redux_elements/Text_Block_Redux.vue":["SdjJ",4],"./container_content_redux_folder/container_redux_elements/input_text_block_redux.vue":["U0L6",3],"./radio_button_list/radio_button.vue":["3lqG"],"./radio_button_list/radio_list.vue":["86rg"],"./text_block.vue":["hHJz"]};s.keys=function(){return Object.keys(o)},s.id="mUJ2",t.exports=s},mXmA:function(t,e){},mg6j:function(t,e,n){"use strict";function s(t){n("08A+")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("MW4G"),i=n("FWz+"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},"nKb+":function(t,e,n){"use strict";var s=n("mvHQ"),o=n.n(s),i=n("7t+N"),a=n.n(i);e.a={name:"Login",props:{should_auto_login:{default:!1}},data:function(){return{random_code:Math.round(1e6*Math.random())+"C"+Math.round(1e7*Math.random())+"LX",logged_in:!1,password:"",name:""}},mounted:function(){window.onload=function(){console.log("GREAT stuff yee"),console.log(this.is_auto_login),console.log("wtf this should log in huh"),console.log(this.is_auto_login),1==this.is_auto_login?(this._show_everything_but_login(),this.password=this.random_code,this.name=this.random_code,this.submit()):this._show_only_login()}.bind(this)},computed:{is_auto_login:function(){return this.should_auto_login}},methods:{logic:function(t,e,n){this.$root.$data.stored_state.clear_user_feedback(),this.$root.$data.stored_state.setNameAndPassword(t,e),this.$root.$data.stored_state.setProjectState(n),this.$root.$data.stored_state.setTask(n),this.$root.$data.stored_state.setInstructions(n),this.$root.$data.stored_state.initialize_session_time_and_start_time(n)},logout:function(){this.$data.logged_in=!1},register_account:function(){},_show_only_login:function(){var t=a.a.noConflict();t("#app").css({visibility:"hidden",display:"block"}),t("#Login_Section").css({visibility:"visible",display:"block"})},_show_everything_but_login:function(){var t=a.a.noConflict();t("#app").css({visibility:"visible",display:"block"}),t("#Login_Section").css({visibility:"hidden",display:"none"})},submit:function(t){return""==this.name||"Invalid Name"==this.name?void(this.name="Invalid Name"):"Invalid Password"==this.password?void(this.password="Invalid Password"):(console.log("password"),console.log(this.password),console.log("name"+this.name),void a.a.ajax({url:"/api/login",data:"jsonData="+o()({name:this.name,password:this.password}),type:"POST",success:function(t){var t=JSON.parse(t);console.log("login request"),console.log(t),"failure"==t.task?(this.name="Wrong Code",this.password="Wrong Code",this.logged_in=!1):(this._show_everything_but_login(),this.logic(this.name,this.password,t))}.bind(this)}))}}}},qh4r:function(t,e,n){"use strict";e.a={name:"Finished",props:{Tasks_Completed:{default:0,type:Number},Code:{default:"-1"}},computed:{compute_work_done:function(){return this.Tasks_Completed>0}}}},uLxJ:function(t,e,n){"use strict";var s,o=n("bOdI"),i=n.n(o),a=n("mvHQ"),r=n.n(a),u=n("7t+N"),_=n.n(u),c=(n("hHJz"),n("hHJz"));e.a=(s={components:{Text_block:c.default},name:"Show_Results",data:function(){return{all_processes:[],prompt:"",result:"",body:"",is_finished:!1,process_id:-1,content:[]}},mounted:function(){this.get_results()},methods:{map_state:function(t){this.prompt=t.prompt,this.result=t.result,this.body=t.body,this.is_finished=t.is_finished,this.process_id=t.process_id,this.all_processes=t.processes_state,this.content=t.content},copy_value:function(t){return console.log(t),console.log("WTF"),t},get_results:function(t){var t=t;_.a.ajax({url:"/api/get_results",data:"jsonData="+r()({id:t}),type:"POST",success:function(t){console.log(t);var t=JSON.parse(t),e=t.results;this.map_state(e)}.bind(this)})}}},i()(s,"mounted",function(){this.get_results(-1)}),i()(s,"computed",{}),s)},uflI:function(t,e,n){"use strict";function s(t){n("GRV1")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("TTDU"),i=n("LQ1U"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},v3TN:function(t,e,n){"use strict";var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"app"}},[t.compute_is_main_page?n("System_Container",{attrs:{should_auto_login:t.should_create_auto_login}}):t._e(),t._v(" "),n("router-view")],1)},o=[],i={render:s,staticRenderFns:o};e.a=i},wu3u:function(t,e){},xJD8:function(t,e,n){"use strict";var s=n("7t+N"),o=(n.n(s),n("uflI"),n("dv9A"),n("l98k"),n("/jgw"),n("xJsL"),n("LqQL"),n("DKMl"),n("hHJz"),n("hjgi"));e.a={name:"app",components:{System_Container:o.default},data:function(){return{should_create_auto_login:!1}},mounted:function(){this.compute_is_main_page},computed:{compute_is_main_page:function(){var t=window.location.href.split("/");return""==t[t.length-1]}}}},xJsL:function(t,e,n){"use strict";function s(t){n("QtPA")}Object.defineProperty(e,"__esModule",{value:!0});var o=n("nKb+"),i=n("BWkt"),a=n("VU/8"),r=s,u=a(o.a,i.a,!1,r,null,null);e.default=u.exports},zXcd:function(t,e,n){"use strict";var s=n("86rg"),o=n("dv9A");e.a={props:["Content","Context","Body_Of_Task","Type","Is_Example","Is_Modifiable","Suggestion_List"],components:{radio_list:s.default,SuggestionList:o.default},data:function(){return{example_text:"THIS IS AN EXAMPLE FOR REFERENCE:",example_explained:" The following text written below is an example of a user taking the content highlighted yellow on the left and rewriting it here\r\n \r\n",user_feedback:"Enter Text Here"}},methods:{lower_opacity_if_example:function(){return this.compute_is_example?"low_opacity":"high_opacity"},background_border_and_red:function(){return["background_red","text_area"]}},computed:{user_input:{get:function(){return this.compute_is_modifiable?this.$root.$data.stored_state.state.current_result:""},set:function(t){this.compute_is_modifiable&&this.$root.$data.stored_state.set_result(t)}},compute_is_modifiable:function(){return void 0!==this.Is_Modifiable&&this.Is_Modifiable},compute_is_example:function(){return void 0===this.Is_Example||this.Is_Example},computed_example_text:function(){return this.compute_is_example?this.example_text:""},computed_explain_text:function(){return this.compute_is_example?this.example_explained:""}}}}},["NHnr"]);
//# sourceMappingURL=app.6ee8aaf0340dcc492e27.js.map