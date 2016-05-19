package losamarillos;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class MainController {

	@RequestMapping("/")
	public String mainpage(Model model) {
		NamesSet ns = new NamesSet();
		model.addAttribute("names", ns.getNames());
		return "index";
	}

	@RequestMapping("/names")
	public @ResponseBody NamesSet names() {
		return new NamesSet();
	}

}
