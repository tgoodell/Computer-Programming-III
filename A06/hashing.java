import java.util.*;
import java.lang.reflect.*;

public class hashing
{
	public static void main(String[] args)
	{
		HashMap<Integer,String> map=new HashMap();
		for(int i=0;i<99;i++)map.add(i,"Asdf"+i);
		System.out.println(map.get(8));
	}
	
	public static long hash(String s)
	{
		long out=0;
		for(char c:s.toCharArray())
		{
			out*=65599;
			out+=(int)(c);
		}
		return (int)out;
	}
}

class HashMap<K,V> // Arguments for a class, can specify type for key K and value V
{
	K[] keys;
	V[] values;
	boolean[] active;
	int INITIAL_SIZE=100;
	int size=0;
	
	public HashMap()
	{
		keys=(K[])(new Object [INITIAL_SIZE]);
		values=(V[])(new Object [INITIAL_SIZE]);
		active=new boolean[INITIAL_SIZE];
	}
	
	public HashMap(int capacity)
	{
		keys=(K[])(new Object [INITIAL_SIZE]);
		values=(V[])(new Object [INITIAL_SIZE]);
		active=new boolean[INITIAL_SIZE];
	}
	
	public void add(K key, V value)
	{
		int index=key.hashCode()%keys.length;
		while(keys[index]!=null)
		{
			index++;
			index%=keys.length;
		}
		keys[index]=key;
		values[index]=value;
		active[index]=true;
		size++;
	}
	
	public boolean isFull()
	{
		return size*10>keys.length*7;
	}
	
	public void upsize()
	{
		HashMap<K,V> temp=new HashMap(keys.length*2);
		for(int i=0;i<keys.length;i++)
		{
			if(keys[i]!=null)
			{
				temp.add(keys[i],values[i]);
			}
		}
		
		this.keys=temp.keys;
		this.values=temp.values;
		this.active=temp.active;
		this.size=temp.size;
	}
	
	public V get(K key)
	{
		int index=key.hashCode()%keys.length;
		
		while(!keys.equals(keys[index]) && active[index])
		{
			index++;
			index%=keys.length;
		}
		if(keys.equals(keys[index]))
		{
			return values[index];
		}
		return null;
	}
	
	public boolean delete(K key)
	{
		int index=key.hashCode()%keys.length;
		
		while(!keys.equals(keys[index]) && active[index])
		{
			index++;
			index%=keys.length;
		}
		if(keys.equals(keys[index]))
		{
			size--;
			keys[index]=null;
			values[index]=null;
			return true;
		}
		return false;
		
	}
}
