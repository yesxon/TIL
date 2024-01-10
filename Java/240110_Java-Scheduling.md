# 240110 Java-Scheduling

### Process Distribution (Scheduling) 구현

- Least Job
- Round Robin
- Priority

### 실습

- Schedule 클래스(인터페이스 혹은 추상클래스)
    - getNextCall( )
    - sendCallToAgent( )
        
        ```java
        package Scheduler;
        
        import java.util.Scanner;
        public interface Schedule {
        
        	String[] cus_list = {"cus1", "cus2", "cus3", "cus4", "cus5", "cus6"};
        	String[] coun_list = {"A", "B", "C"};
        	Integer[] priority = {3, 2, 1, 4, 5, 6};
        	Integer[] time = {1,2,3,4,5,2};
        	
        	public void getNextCall();//추상메소드
        	public void sendCallToAgent();
        	
        	// 클래스함수 static method <-> instance method 
        		// 인스턴스.함수(); 로만 실행이 가능한, 인스턴스를 만들어야만 사용할 수 있는 게 아니라
        		// 클래스.함수();로 실행할 수 있는 -> 객체가 아닌 클래스에 속한 함수이므로
        		// 인스턴스가 변경되었다고 클래스 함수의 내용이 변경되지 않는다 
        		// -> 클래스에서도 인스턴스에서도 접근 가능
        	
        	public static void run() {
        		Scanner sc = new Scanner(System.in);
        		int flag = 1;
        		while(flag == 1) {
        			
        			String a = sc.next();
        			if (a.toLowerCase().equals("p")) {
        				Priority prior = new Priority();
        				prior.getNextCall();
        				prior.sendCallToAgent();
        			}
        			else if(a.toLowerCase().equals("r")) {
        				RoundRobin round = new RoundRobin();
        				round.getNextCall();
        				round.sendCallToAgent();
        			}
        			else if (a.toLowerCase().equals("l")) {
        				LeastJob least = new LeastJob();
        				least.getNextCall();
        				least.sendCallToAgent();
        			}
        			else if (a.toLowerCase().equals("q")) {
        				System.out.println("시스템종료");
        				flag = 0;
        			}
        			else {
        				System.out.println("제대로입력");
        				continue;
        			}
        			
        		}
        		sc.close();
        	}
        
        }
        ```
        
    - 
        - Least Job
            - 대기열에서 고객을 순서대로 넘김
            - 대기열 가장 짧은 상담원에게 배분
                
                ```java
                package Scheduler;
                
                import java.util.*;
                
                public class LeastJob implements Schedule {
                	@Override
                	public void getNextCall() {
                		System.out.println("- 1. 대기열에서 고객을 순서대로 넘깁니다.");
                		
                		String[] cus_list = Schedule.cus_list;
                		ArrayList<String> cus_array = new ArrayList<>(Arrays.asList(cus_list));
                		System.out.println(String.format("고객 순서:"+ cus_array));
                	}
                	
                	@Override
                	public void sendCallToAgent() {
                		System.out.println("- 2. 상담전화 대기열이 가장 짧은 상담원에게 배분합니다.");
                		Map<String, ArrayList<String>> coun_map = new HashMap<>();
                		String[] cus_list = Schedule.cus_list;
                		String[] coun_list = Schedule.coun_list;
                		
                		for (int i = 1; i <= coun_list.length; i++) {
                			coun_map.put(coun_list[i-1], new ArrayList<>());
                			coun_map.get(coun_list[i-1]).add(cus_list[i-1]);
                			coun_map.get(coun_list[i-1]).add(cus_list[i - 1 + cus_list.length/2]);
                		}
                		System.out.println(coun_map);
                	}
                }
                ```
                
        - Round Robin
            - 고객은 순서대로 넘김
            - 전화를 마친 상담원에게 배분
                
                ```java
                package Scheduler;
                import java.util.*;
                
                public class RoundRobin implements Schedule {
                	ArrayList<String> cus_array = new ArrayList<>();
                	
                	@Override
                	public void getNextCall() {
                //		System.out.println("- 1. 대기열에서 고객을 순서대로 넘깁니다.");	
                		
                		String[] cus_list = Schedule.cus_list;
                		ArrayList<String> cus_arr = new ArrayList<>(Arrays.asList(cus_list));
                		this.cus_array = cus_arr;
                //		System.out.println(String.format("고객 순서:"+ this.cus_array));
                	}
                	
                	
                	
                	@Override
                	public void sendCallToAgent() {
                		System.out.println("- 2. 상담전화를 전화를 마친 상담원에게 배분합니다.");
                		
                		Integer[] time_list = Schedule.time;
                		String[] coun_list = Schedule.coun_list;
                		SortedMap<String, Integer> cus_map = new TreeMap<>();
                		
                		// coun_map 생성
                		Map<String, ArrayList<String>> coun_map = new HashMap<>();
                		for (int i = 0; i < coun_list.length; i++) {
                			coun_map.put(coun_list[i], new ArrayList<>());
                		}
                		
                		// {고객=시간}
                		for (int i = 0; i < this.cus_array.size(); i++) {
                			cus_map.put(this.cus_array.get(i), time_list[i]);
                		}
                		System.out.println("고객 ArrayList" + this.cus_array);
                		System.out.println("고객 map" + cus_map);
                		System.out.println("상담사 map" + coun_map);
                		
                		
                		
                		for (int i = -1; i < this.cus_array.size(); i++) {
                			int min_v = cus_map.values().stream().min(Integer::compare).get();
                			int while_flag = 0;
                			
                			// map에서 값이 0인 원소 삭제
                			while (min_v == 0) {
                				// 가장 작은 값 찾기
                		        Map.Entry<String, Integer> minEntry = null;
                		        
                		        for (Map.Entry<String, Integer> entry : cus_map.entrySet()) {
                		            if (minEntry == null || entry.getValue() < minEntry.getValue()) {
                		                minEntry = entry;
                		            }
                		        }
                		        
                		        
                		        if (minEntry != null) {
                		        	if (i < 3) {
                		        		if (coun_map.get(coun_list[i]).size() > 0) {
                			        		break;
                			        		}
                	        			coun_map.get(coun_list[i]).add(minEntry.getKey());
                			        	cus_map.remove(minEntry.getKey());
                				   
                			        	System.out.println("대기열: " + cus_map);
                				        System.out.println("상담원이 맡고있는 고객: " + coun_map);
                						min_v = cus_map.values().stream().min(Integer::compare).get();
                			        		
                		        		
                		        	} else if (i >= 3) {
                		        		
                		        		if (coun_map.get(coun_list[i - 3]).size() > 1) {
                			        		break;
                			        		}
                		        		
                	        			coun_map.get(coun_list[i - 3]).add(minEntry.getKey());
                			        	cus_map.remove(minEntry.getKey());
                				   
                				        System.out.println("대기열: " + cus_map);
                				        System.out.println("상담원이 맡고있는 고객: " + coun_map);
                				        
                				        
                				        if (cus_map.size() == 0) {
                				        	min_v = 0;
                				        	} else {
                				        		min_v = cus_map.values().stream().min(Integer::compare).get();
                				        	}
                				        
                				        
                				        }
                		        	} else if (minEntry == null) {
                		        		// min_v을 0이 아닌 값으로 변경
                		        		min_v = 999;
                		        		break;
                		        	}
                				}
                			
                			if (min_v > 0) {
                				if (cus_map.size() != 0) {
                					System.out.println("----------------------------------");
                					for (Map.Entry<String, Integer> entry : cus_map.entrySet()) {
                			            entry.setValue(entry.getValue() - 1);
                			        }
                				}
                			}
                		}
                		
                		System.out.println("최종 ------------------------------");
                		System.out.println(coun_map);
                		
                	}	
                }
                ```
                
        - Priority
            - 우선순위 높은 고객 줄 세움
            - 일 잘하는 상담원에게 배분
                
                ```java
                package Scheduler;
                
                import java.util.*;
                
                public class Priority implements Schedule {
                	@Override
                	public void getNextCall() {
                		System.out.println("- 1. 대기열에서 고객을 순서대로 넘깁니다.");
                		
                		String[] cus_list = Schedule.cus_list;
                		for (String cus : cus_list) {
                			System.out.println(cus);
                		}
                	}
                	
                	@Override
                	public void sendCallToAgent() {
                		System.out.println("- 2. 상담전화 우선순위가 가장 높은 상담원에게 배분합니다.");
                		Map<String, ArrayList<String>> coun_map = new HashMap<>();
                		String[] cus_list = Schedule.cus_list;
                		String[] coun_list = Schedule.coun_list;
                		Integer[] priority = Schedule.priority;
                		
                		ArrayList<String> priorCusList = new ArrayList<>();
                		for (int i = 0; i < cus_list.length; i++) {
                			String[] tmp = {Integer.toString(priority[i]), cus_list[i]};
                			ArrayList<String> priorCusList2 = new ArrayList<>(Arrays.asList(tmp)) ;
                			System.out.println(priorCusList2);
                		}
                
                //		for (int i = 1; i <= coun_list.length; i++) {
                //			coun_map.put(coun_list[i-1], new ArrayList<String>());
                //			coun_map.get(coun_list[i-1]).add(priorCusList[i - 1]);
                //			coun_map.get(coun_list[i-1]).add(priorCusList[i - 1 + cus_list.length/2]);
                //		}
                		
                		System.out.println(coun_map);
                	}
                }
                ```